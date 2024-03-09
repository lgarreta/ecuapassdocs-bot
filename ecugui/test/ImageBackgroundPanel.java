
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class ImageBackgroundPanel extends JPanel {

	private BufferedImage backgroundImage;
	private JTextField textField1;
	private JTextField textField2;

	public ImageBackgroundPanel () {
		// Load the image for the background
		try {
			backgroundImage = ImageIO.read (new File ("/home/lg/BIO/iaprojects/apps/app-importacion/resources/code/cartaporte-form/ecuapass_form.png"));
		} catch (IOException e) {
			e.printStackTrace ();
		}

		// Set the layout to null to allow custom positioning of components
		setLayout (null);

		// Create and position the text fields
		textField1 = new JTextField ();
		textField1.setBounds (50, 50, 200, 30);

		textField2 = new JTextField ();
		textField2.setBounds (50, 100, 200, 30);

		// Add the text fields to the panel
		add (textField1);
		add (textField2);
	}

	@Override
	protected void paintComponent (Graphics g) {
		super.paintComponent (g);

		// Draw the background image
		if (backgroundImage != null) {
			int width = backgroundImage.getWidth ();
			int height = backgroundImage.getHeight ();

			// Calculate the position to center the image on the panel
			int x = (getWidth () - width) / 2;
			int y = (getHeight () - height) / 2;

			g.drawImage (backgroundImage, x, y, width, height, this);
		}
	}

	public static void main (String[] args) {
		SwingUtilities.invokeLater (() -> {
			JFrame frame = new JFrame ("Image Background Panel Example");
			frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);
			frame.setSize (400, 300);

			// Create an instance of the ImageBackgroundPanel
			ImageBackgroundPanel panel = new ImageBackgroundPanel ();

			// Add the panel to the frame
			frame.add (panel);

			frame.setVisible (true);
		});
	}
}
