import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class InitialConfigDialog extends JDialog {
    public InitialConfigDialog(JFrame parent) {
        super(parent, "Initial Configuration", true); // true for modal

        JPanel panel = new JPanel(new GridLayout(2, 2));
        panel.add(new JLabel("Parameter 1:"));
        panel.add(new JTextField());
        panel.add(new JLabel("Parameter 2:"));
        panel.add(new JTextField());

        JButton okButton = new JButton("OK");
        okButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // Process configuration parameters here
                dispose(); // Close the dialog
            }
        });

        JButton cancelButton = new JButton("Cancel");
        cancelButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                dispose(); // Close the dialog
            }
        });

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(okButton);
        buttonPanel.add(cancelButton);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(panel, BorderLayout.CENTER);
        getContentPane().add(buttonPanel, BorderLayout.SOUTH);

        pack();
        setLocationRelativeTo(parent); // Center dialog relative to parent window
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                JFrame frame = new JFrame();
                frame.setSize(400, 300);
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setVisible(true);

                InitialConfigDialog dialog = new InitialConfigDialog(frame);
                dialog.setVisible(true);
            }
        });
    }
}

