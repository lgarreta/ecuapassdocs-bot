import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class PythonScriptRunner {
    private static Process process;

    public static void main(String[] args) {
        JFrame frame = new JFrame("Python Script Runner");
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        frame.add(panel);
        placeComponents(panel);

        frame.setVisible(true);
    }

    private static void placeComponents(JPanel panel) {
        panel.setLayout(null);

        JLabel userLabel = new JLabel("Number:");
        userLabel.setBounds(10, 20, 80, 25);
        panel.add(userLabel);

        JTextField numberText = new JTextField(20);
        numberText.setBounds(100, 20, 165, 25);
        panel.add(numberText);

        JButton runButton = new JButton("Run Script");
        runButton.setBounds(10, 80, 150, 25);
        panel.add(runButton);

        JButton cancelButton = new JButton("Cancel");
        cancelButton.setBounds(200, 80, 150, 25);
        panel.add(cancelButton);

        JTextArea outputArea = new JTextArea();
        outputArea.setBounds(10, 110, 350, 150);
        panel.add(outputArea);

        runButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String number = numberText.getText();
                outputArea.setText("Running script...");
                new Thread(() -> runPythonScript(number, outputArea)).start();
            }
        });

        cancelButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (process != null) {
                    process.destroy();
                    outputArea.append("\nScript cancelled.");
                }
            }
        });
    }

    private static void runPythonScript(String number, JTextArea outputArea) {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python", "flask_and_selenium.py", number);
            processBuilder.redirectErrorStream(true);
            process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                String finalLine = line;
                SwingUtilities.invokeLater(() -> outputArea.append(finalLine + "\n"));
            }

            process.waitFor();
            SwingUtilities.invokeLater(() -> outputArea.append("Process completed with exit code: " + process.exitValue()));
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            SwingUtilities.invokeLater(() -> outputArea.setText("Error running script: " + e.getMessage()));
        }
    }
}
