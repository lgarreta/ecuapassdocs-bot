package results;

import documento.DocModel;
import documento.DocRecord;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.FocusTraversalPolicy;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;

// View class containing a panel with labe and icon image
public class EcuapassPanel extends JPanel {

	public DocRecord record;
	JLabel imageLabel;
	JPanel imagePanel;
	ImageIcon imageIcon;
	Dimension size;

	public EcuapassPanel (URL imgPath) {
		imageIcon = new ImageIcon (imgPath);

		imageLabel = new JLabel (imageIcon);
		size = new Dimension (imageIcon.getImage ().getWidth (null), imageIcon.getImage ().getHeight (null));
		imagePanel = new JPanel (null);
		imagePanel.setSize (size);
		imagePanel.setMaximumSize (size);
		imagePanel.setMinimumSize (size);
		imagePanel.setPreferredSize (size);

		imagePanel.add (imageLabel);
		imagePanel.setPreferredSize (size);

		JScrollPane scroll = new JScrollPane (imagePanel);
		add (scroll);

		// Add the MouseWheelListener to the JScrollPane
		imagePanel.addMouseWheelListener (new MouseWheelListener () {
			@Override
			public void mouseWheelMoved (MouseWheelEvent e) {
				// Adjust the vertical scroll bar based on the mouse wheel movement
				int scrollAmount = e.getUnitsToScroll ();
				JScrollBar verticalScrollBar = ((JScrollPane) getParent ().getParent ()).getVerticalScrollBar ();
				verticalScrollBar.setUnitIncrement (20);
				int currentValue = verticalScrollBar.getValue ();
				verticalScrollBar.setValue (currentValue + scrollAmount * verticalScrollBar.getUnitIncrement ());
			}
		});
	}

	public Component[] getComponents () {
		return (imagePanel.getComponents ());
	}

	public void addFields (ArrayList<Component> inputFields) {
		remove (imageLabel);
		for (Component cmp : inputFields) {
			imagePanel.add (cmp);
		}
		imagePanel.add (imageLabel);
		imageLabel.setBounds (0, 0, size.width, size.height);

		// Create a custom focus traversal policy
		Component components[] = inputFields.toArray(new Component[inputFields.size()]);
		FocusTraversalPolicy customPolicy = new CustomFocusTraversalPolicy (components);
		imagePanel.setFocusTraversalPolicy (customPolicy);
	}

	public void setComponentsFocusOrder () {

	}

	public static void main (String args[]) {
		try {
			DocModel doc = new DocModel ();
			doc.initGlobalPaths ();

			JFrame jf = new JFrame ();
			jf.setSize (967, 1314);

			// Create a JPanel to hold content
			URL imgPath = new URL ("/home/lg/BIO/iaprojects/ecuapass/cartaportes/ecugui/resources/images/image-cartaporte-ecuapass.png");
			EcuapassPanel ev = new EcuapassPanel (imgPath);
			//JScrollPane scrollPane = new JScrollPane (contentPanel);

			// Add the JScrollPane to the JFrame
			jf.add (ev);
			jf.setVisible (true);
		} catch (MalformedURLException ex) {
			Logger.getLogger (EcuapassPanel.class.getName ()).log (Level.SEVERE, null, ex);
		}
	}

}