package widgets;


import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

public class CountrySelectionDialogGPT {

    public static void main(String[] args) {
        showCountryDialog();
    }

    private static void showCountryDialog() {
        // Create buttons with country flags
        JButton colombiaButton = new JButton("Colombia", new ImageIcon("colombia_flag.png"));
        JButton ecuadorButton = new JButton("Ecuador", new ImageIcon("ecuador_flag.png"));

        // Create a panel to hold the buttons
        JPanel panel = new JPanel();
        panel.add(colombiaButton);
        panel.add(ecuadorButton);

        // Create the option pane with the custom panel
        JOptionPane optionPane = new JOptionPane(panel, JOptionPane.PLAIN_MESSAGE, JOptionPane.DEFAULT_OPTION, null, new Object[]{}, null);

        // Create the dialog and set it as modal
        JDialog dialog = optionPane.createDialog("Select a Country");
        dialog.setModal(true);

        // Add action listeners to the buttons
        colombiaButton.addActionListener(e -> {
            // Handle the selection of Colombia
            System.out.println("Colombia selected");
            dialog.dispose(); // Close the dialog
        });

        ecuadorButton.addActionListener(e -> {
            // Handle the selection of Ecuador
            System.out.println("Ecuador selected");
            dialog.dispose(); // Close the dialog
        });

        // Set default close operation and make the dialog visible
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
    }
}
