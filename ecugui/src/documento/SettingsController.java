package documento;

// Class to write/read initial settings as "empresa", "creator URL", "ecuapass URL"
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;
import java.awt.Component;
import java.awt.HeadlessException;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class SettingsController {

	String company;
	String creatorURL;
	String ecuapassURL;

	Component parent;
	SettingsDialog dialog;
	String companiesString;
	String runningPath;

	public SettingsController (Component parent, String companiesString, String runningPath) {
		this.parent = parent;
		this.companiesString = companiesString;
		this.runningPath = runningPath;
	}

	// First time initialization. Set "empresa" name for  cloud document models
	public String initCurrentWorkingCompany () {
		String companyName = null;
		File settingsFile = new File (runningPath + "/settings.txt");
		System.out.println (">>> Settings file: " + settingsFile);

		try {
			if (settingsFile.exists ()) {// Load company name
				companyName = this.getValue ("empresa");
				
			}else { // Request company name
				/*
				 * JFrame settingsFrame = new JFrame ("Configuración Inicial");
				 * settingsFrame.setContentPane (new SettingsPanel ());
				 * settingsFrame.setVisible (true); settingsFrame.setSize (700, 150);
				 */
				dialog = new SettingsDialog ((JFrame) this.parent, true);
				dialog.setController (this);
				dialog.setVisible (true);
				/*
				 * JTextField textField = new JTextField (); Object[] message = {"Nombre
				 * de la empresa:", textField}; Object[] options = {"Aceptar",
				 * "Cancelar"}; /*while (true) { JFrame settingsFrame = new JFrame
				 * ("Configuración Inicial"); settingsFrame.setContentPane (new
				 * SettingsPanel());
				 *
				 * int option = JOptionPane.showOptionDialog (null, message,
				 * "Configuración Inicial de la Empresa", JOptionPane.DEFAULT_OPTION,
				 * JOptionPane.INFORMATION_MESSAGE, null, options, null);
				 *
				 * if (option == JOptionPane.OK_OPTION) { companyName =
				 * textField.getText ().toUpperCase (); if (companyName.matches
				 * (companiesString)) { SettingsController.init (companyName,
				 * runningPath); break; } } else System.exit (0); }
				 */

			}
			System.out.println (">>>>>>>>> Empresa: " + companyName + " <<<<<<<<<<");
		} catch (HeadlessException ex) {
			ex.printStackTrace ();
		}
		return companyName;
	}

	public void onSaveButton () {
		while (true) {
			String companyName = dialog.getCompanyName ().toUpperCase ();
			if (companyName.matches (this.companiesString)) {
				this.init (companyName, runningPath);
				dialog.dispose ();
				break;
			} else
				System.exit (0);
		}
	}
		// Int"settings.json" file located in "runningPath"
	public void init (String companyName, String runningPath) {
		// Create a JSON object
		JsonObject jsonObject = new JsonObject ();
		jsonObject.add ("empresa", new JsonPrimitive (companyName));
		jsonObject.add ("url_creador", new JsonPrimitive (dialog.getDocsCreatorURL ()));
		jsonObject.add ("url_ecuapass", new JsonPrimitive (dialog.getEcuapassURL ()));
		jsonObject.add ("global_pause", new JsonPrimitive ("0.05"));
		jsonObject.add ("slow_pause", new JsonPrimitive ("0.1"));

		// Specify the file path
		File settingsFile = new File (runningPath + "/settings.txt");
		// Create Gson instance with indentation
		Gson gson = new GsonBuilder ().setPrettyPrinting ().create ();
		// Convert the JSON object to a JSON-formatted string
		String jsonString = gson.toJson (jsonObject);

		// Write the JSON string to a file
		try (FileWriter fileWriter = new FileWriter (settingsFile)) {
			System.out.println (">>> Guardando archivo de configuracion: " + settingsFile);
			fileWriter.write (jsonString);
		} catch (Exception e) {
			e.printStackTrace ();
		}
	}

	// Get value from "settings.json" file located in "runningPath"
	public String getValue (String key) {
		File settingsFile = new File (this.runningPath + "/settings.txt");

		String value = null;
		try {
			JSONParser parser = new JSONParser ();
			JSONObject jsonObj = (JSONObject) parser.parse (new FileReader (settingsFile));
			value = (String) jsonObj.get (key);

		} catch (IOException | ParseException ex) {
			Logger.getLogger (SettingsController.class
				.getName ()).log (Level.SEVERE, null, ex);
		}
		return value;
	}

	// Set value into "settings.json" file located in "runningPath"
	public static void setValue (String key, String value, String runningPath) {
		File settingsFile = new File (runningPath + "/settings.txt");

		// Create or update JSON data
		JSONObject jsonData = new JSONObject ();
		jsonData.put (key, value);
		// Write or update the JSON file
		try {
			writeJsonToFile (settingsFile.toString (), jsonData);
		} catch (IOException | ParseException e) {
			e.printStackTrace ();
		}
	}

	private static void writeJsonToFile (String filePath, JSONObject jsonData) throws IOException, ParseException {
		// Read existing JSON data and update the value
		JSONObject existingData = readJsonFromFile (filePath);
		existingData.putAll (jsonData);

		// Write the updated JSON data to the file
		try (FileWriter fileWriter = new FileWriter (filePath)) {
			fileWriter.write (existingData.toJSONString ());
		}
	}

	private static JSONObject readJsonFromFile (String filePath) throws IOException, ParseException {
		JSONParser parser = new JSONParser ();
		try (FileReader fileReader = new FileReader (filePath)) {
			return (JSONObject) parser.parse (fileReader);
		}
	}
}
