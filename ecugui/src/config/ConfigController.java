package config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import documento.DocModel;
import java.awt.HeadlessException;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import main.Controller;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import widgets.InitialSettingsDialog;

public class ConfigController {

	String runningPath = DocModel.runningPath;
	InitialSettingsDialog initialSettingsDialog;
	public FeedbackView feedbackView;
	Controller controller;

	public ConfigController (Controller controller) {
		this.controller = controller;
		feedbackView = new FeedbackView ();
		feedbackView.setController (this);
	}

	public void onSendFeedback (String feedbackText) {
		controller.onSendFeedback (feedbackText);
	}

	// First time initialization. Set "empresa" name for  cloud document models
	public String initSettings (JFrame parent) {
		String companyName = null;
		try {
			File settingsFile = new File (runningPath + "/settings.txt");
			System.out.println (">>> Settings file: " + settingsFile);
			if (settingsFile.exists () == false) {// Load nombreEmpresa name
				initialSettingsDialog = new InitialSettingsDialog (parent);
				initialSettingsDialog.setController (this);
				initialSettingsDialog.startProcess ();
			}
			JSONObject settings = new JSONObject ();
			JSONParser parser = new JSONParser ();
			settings = (JSONObject) parser.parse (new FileReader (settingsFile));
			this.feedbackView.setSettings (settings);
			companyName = (String) settings.get ("empresa");
			System.out.println (">>>>>>>>> Empresa: " + companyName + " <<<<<<<<<<");
		} catch (FileNotFoundException ex) {
			Logger.getLogger (ConfigController.class.getName ()).log (Level.SEVERE, null, ex);
		} catch (IOException | ParseException ex) {
			Logger.getLogger (ConfigController.class.getName()).log (Level.SEVERE, null, ex);
		}
		return companyName;
	}

	public void onSaveSettings (JSONObject settings) {
		if (this.checkForValidSettings (settings) == false)
			return;

		if (this.initialSettingsDialog != null)
			this.initialSettingsDialog.endProcess ();

		File settingsFile = new File (runningPath + "/settings.txt");
		Gson gson = new GsonBuilder ().setPrettyPrinting ().create ();
		String jsonString = gson.toJson (settings);

		// Write the JSON string to a file
		try (FileWriter fileWriter = new FileWriter (settingsFile)) {
			System.out.println (">>> Guardando archivo de configuracion: " + settingsFile);
			fileWriter.write (jsonString);
		} catch (Exception e) {
			e.printStackTrace ();
		}
	}

	public void onCancelSettings () {
		if (this.initialSettingsDialog != null)
			System.exit (0);
	}

	public boolean checkForValidSettings (JSONObject settings) {
		if (settings.get ("empresa").equals ("")) {
			JOptionPane.showMessageDialog (null, "Nombre de empresa inválido");
			return false;
		}
		if (settings.get ("codebin_url").equals ("")) {
			JOptionPane.showMessageDialog (null, "URL Codebin inválido");
			return false;
		}
		if (settings.get ("codebin_user").equals ("")) {
			JOptionPane.showMessageDialog (null, "Usuario Codebin inválido");
			return false;
		}
		if (settings.get ("codebin_password").equals ("")) {
			JOptionPane.showMessageDialog (null, "Contraseña Codebin inválido");
			return false;
		}
		return true;
	}

	// Get value from "settings.json" file located in "runningPath"
	public String getSettingsValue (String key) {
		File settingsFile = new File (this.runningPath + "/settings.txt");

		String value = null;
		try {
			JSONParser parser = new JSONParser ();
			JSONObject jsonObj = (JSONObject) parser.parse (new FileReader (settingsFile));
			value = (String) jsonObj.get (key);

		} catch (IOException | ParseException ex) {
			Logger.getLogger (ConfigController.class
				.getName ()).log (Level.SEVERE, null, ex);
		}
		return value;
	}
}
