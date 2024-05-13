package widgets;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import config.ConfigController;
import documento.DocModel;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.FileWriter;
import org.json.simple.JSONObject;

// Creates a dialog for waiting to finish or cancel the document processing
public class InitialSettingsDialog {

	private static final int DIALOG_WIDTH = 600;
	private static final int DIALOG_HEIGHT = 300;

	private JFrame mainFrame;
	private JDialog initialDialog;
	private JLabel messageLabel;

	private config.SettingsPanel settingsPanel;
	private ConfigController configController;

	public InitialSettingsDialog (JFrame mainFrame) {
		this.mainFrame = mainFrame;
		//configController = new ConfigController (null);
	}

	public void setController (ConfigController controller) {
		this.configController = controller;
	}

	public void startProcess () {
		//mainFrame.setEnabled (false);

		initialDialog = new JDialog (mainFrame, "Configuración Inicial...", Dialog.ModalityType.APPLICATION_MODAL);
		initialDialog.setSize (DIALOG_WIDTH, DIALOG_HEIGHT);
		initialDialog.setResizable (true);
		initialDialog.setLocationRelativeTo (mainFrame);
		initialDialog.setLayout (new BorderLayout ());
		initialDialog.setDefaultCloseOperation (WindowConstants.DO_NOTHING_ON_CLOSE);

		messageLabel = new JLabel ("Analizando documentos...");
		settingsPanel = new config.SettingsPanel ();
		settingsPanel.setController (configController);

		JPanel labelPanel = new JPanel (new FlowLayout ());
		labelPanel.add (messageLabel);

		initialDialog.add (labelPanel, BorderLayout.NORTH);
		initialDialog.add (settingsPanel, BorderLayout.CENTER);

		initialDialog.setVisible (true);
	}

	public void endProcess () {
		initialDialog.dispose ();
	}

	public static void main (String[] args) {
		DocModel.runningPath = "/home/lg";
		InitialSettingsDialog pd = new InitialSettingsDialog (null);
		pd.startProcess ();
	}
}
