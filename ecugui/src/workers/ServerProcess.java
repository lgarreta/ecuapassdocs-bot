package workers;

import documento.DocModel;
import documento.DocRecord;
import java.awt.Frame;
import main.Controller;
import main.MainController;
import main.Utils;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.List;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;
import widgets.TopMessageDialog;

/*
 * Execute command line app with parameters. Outputs are sent to controller to
 * show them in both console and view.
 */
public class ServerProcess {

	Controller controller;
	DocModel docModel;
	Process process;

	String serverUrl; // Server address and entry point
	ArrayList<String> commandList; // Command line as list

	public ServerProcess (Controller controller, DocModel docModel) {
		this.controller = controller;
		this.docModel = docModel;
		serverUrl = this.getServerUrl (5000); // Server address and entry point	
	}

	// Send message to server to start a process using data
	public boolean startProcess (String service, String data1, String data2) {
		try {
			// Create URL and open connection
			URL url = new URL (this.serverUrl);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection ();

			// Set up the connection for a POST request
			connection.setRequestMethod ("POST");
			connection.setRequestProperty ("Content-Type", "application/json");
			connection.setDoOutput (true);

			// Create JSON payload and write it to the connection's output stream
			String formatStr = "{\"%s\":\"%s\", \"%s\":\"%s\", \"%s\":\"%s\"}";
			String jsonPayload = String.format (formatStr, "service", service, "data1", data1, "data2", data2);
			System.out.println ("+++ payload" + jsonPayload);
			try (OutputStream os = connection.getOutputStream ()) {
				byte[] input = jsonPayload.getBytes (StandardCharsets.UTF_8);
				os.write (input, 0, input.length);
			}
			// Read response. You can read and process the response here if needed
			int responseCode = connection.getResponseCode ();
			if (responseCode != HttpURLConnection.HTTP_OK) {
				controller.out ("ERROR: Enviando solicitud. Código de respuesta: " + responseCode);
				return false;
			}
		} catch (java.net.ConnectException ex) {
			controller.out ("Servidor desconectado");
		} catch (IOException ex) {
			ex.printStackTrace ();
		}
		return true;
	}

	// Handle server intermediate results received durint thread execution
	protected void process (List chunks) {
		for (Object obj : chunks) {
			String statusMsg = obj.toString ();
			controller.out (statusMsg);
			// Check if cloud process ended successfully
			if (statusMsg.contains ("Análisis exitoso del documento"))
				controller.onEndProcessing ("EXITO", statusMsg);
			else if (statusMsg.contains ("Finalizando servidor Ecuapass")) {
				System.out.println (">>> CLIENTE: Finalizando servidor Ecuapass");
				System.exit (0);
			} else if (statusMsg.contains ("SERVER: ERROR:"))
				controller.onEndProcessing ("ERROR", statusMsg);
			else if (statusMsg.contains ("Documento no encontrado"))
				controller.onEndProcessing ("ERROR", statusMsg);
			else if (statusMsg.contains ("SERVER: ALERTA:")) {
				// Display to user'ALERTA' messages 
				statusMsg = statusMsg.split ("ALERTA:")[1];
				TopMessageDialog dialog = new TopMessageDialog (controller.getMainView (), statusMsg);
			} else if (statusMsg.contains ("SERVER: MENSAJE:")) {
				// Display to user'ALERTA' messages 
				// Hide the main frame
				controller.getMainView ().setState (Frame.ICONIFIED);
				statusMsg = statusMsg.split ("MENSAJE:")[1];
				TopMessageDialog dialog = new TopMessageDialog (controller.getMainView (), statusMsg);
			} else if (statusMsg.contains ("Server is running on port")) {
				String portString = statusMsg.split ("::")[1].trim ();
				int urlPortNumber = Integer.parseInt (portString);
				this.serverUrl = this.getServerUrl (urlPortNumber); // Server address and entry point	
				controller.onServerRunning (urlPortNumber);
			} else if (statusMsg.contains ("FEEDBACK:")) {	// Server sends feedback
				String docFilepath = statusMsg.split ("'")[1];
				controller.onSendFeedback (docFilepath);
			} else if (statusMsg.contains ("Problemas procesando documento"))
				controller.onEndProcessing ("ERROR", statusMsg);
		}
	}

	// Start the server process and publish its messages
	public void execute () {
		this.createExecutableCommand ();
		if (this.copyResourcesToTempDir ())
			controller.out ("CLIENTE: Ejecutándose el servidor: " + commandList);
		else
			controller.out ("ERROR: No se pudo copiar recursos.");

		try {
			ProcessBuilder processBuilder = new ProcessBuilder (commandList);
			processBuilder.redirectErrorStream (true);
			process = processBuilder.start ();
			// Handle the response
			System.out.println ("+++ Handling the response...");
			new Thread (() -> {
				this.handleServerResponse (process);
			}).start ();

			process.waitFor ();
		} catch (IOException | InterruptedException e) {
			e.printStackTrace ();
		}
	}

	// Handle the response from the server
	public boolean handleServerResponse (Process process) {
		try {
			// Read the response (optional)
			BufferedReader reader = new BufferedReader (new InputStreamReader (process.getInputStream ()));
			String line;
			while ((line = reader.readLine ()) != null) {
				//controller.out (line);
				List<String> chunks = Arrays.asList (line);
				this.process (chunks);
			}
			reader.close ();
			return true;
		} catch (IOException ex) {
			Logger.getLogger (ServerWorker.class.getName ()).log (Level.SEVERE, null, ex);
		}
		return false;
	}

	// Stop the process forcefully
	public void cancel (boolean byForce) {
		process.destroyForcibly ();
	}

	// Create the URL reading a port number in a file 'url_port.txt" written by main python program
	public String getServerUrl () {
		String fileName = "url_port.txt";
		BufferedReader reader = null;
		int portNumber = 5000;

		try {
			reader = new BufferedReader (new FileReader (fileName));
			String line = reader.readLine (); // Read the first line
			if (line != null) {
				portNumber = Integer.parseInt (line); // Convert the string to an integer
				System.out.println ("+++ The portNumber in the file is: " + portNumber);
			}
		} catch (IOException e) {
			e.printStackTrace ();
		} catch (NumberFormatException e) {
			System.out.println ("+++ The file does not contain a valid integer.");
		} finally {
			try {
				if (reader != null)
					reader.close (); // Close the BufferedReader
			} catch (IOException e) {
				e.printStackTrace ();
			}
		}

		String urlString = this.getServerUrl (portNumber);
		return urlString;
	}

	//-----------------------------------------------------------------	
	// Create command list according to the OS, service, and parameters
	//--------------------------------------------------------	-------
	public void createExecutableCommand () {
		String OS = System.getProperty ("os.name").toLowerCase ();
		String separator = OS.contains ("windows") ? "\\" : "/";

		// For testing: python .py, for production: windows .exe
		String exeProgram = "ecuapass_server" + separator + "ecuapass_server.exe";
		String pyProgram = "ecuserver" + separator + "ecuapass_server.py";

		String command = "";
		if (OS.contains ("windows"))
			if (DocModel.runningPath.contains ("test")) {
				command = Paths.get (docModel.runningPath, pyProgram).toString ();
				commandList = new ArrayList<> (Arrays.asList ("cmd.exe", "/c", "python", command));
			} else {
				command = Paths.get (docModel.runningPath, exeProgram).toString ();
				commandList = new ArrayList<> (Arrays.asList (command));
			}
		else {
			command = Paths.get (docModel.runningPath, pyProgram).toString ();
			commandList = new ArrayList<> (Arrays.asList ("python3", command));
		}
	}

	// Create the URL using a port number sent by the 'printx' server
	public String getServerUrl (int urlPortNumber) {
		serverUrl = String.format ("http://127.0.0.1:%s/start_processing", urlPortNumber);
		return serverUrl;
	}

	// Copy input files in 'DocModel' to new working dir with new docType name
	public void copyDocToProjectsDir (DocRecord docRecord) {
		docModel.createFolder (docModel.projectsPath);
		File docFilepath = new File (docRecord.docFilepath);
		File destFilepath = new File (docModel.projectsPath, docRecord.docTypeFilename);
		Utils.copyFile (docFilepath.toString (), destFilepath.toString ());

		// Copy cache document in pickle file
		File docCacheFilepath = new File (Utils.getResultsFile (docRecord.docFilepath, "CACHE.pkl"));
		docRecord.docFilepath = destFilepath.toString ();
		if (docCacheFilepath.exists ()) {
			destFilepath = new File (docModel.projectsPath, docCacheFilepath.getName ());
			Utils.copyFile (docCacheFilepath.toString (), destFilepath.toString ());
		}
	}

	// Copy emmbeded resources	(programs and images) to temporal dir
	public boolean copyResourcesToTempDir () {
		docModel.createFolder (docModel.temporalPath + "/" + "resources");
		if (this.copyResourcesFromJarToTempDir ())
			controller.out ("CLIENTE: Copiando recursos desde un JAR.");
		else if (this.copyResourcesFromPathToTempDir ())
			controller.out ("CLIENTE: Copiando recursos desde un PATH.");
		else {
			JOptionPane.showMessageDialog (null, "No se pudieron copiar los recursos necesarios para la ejecución!");
			return false;
		}
		return true;
	}

	public boolean copyResourcesFromJarToTempDir () {
		try {
			String resourceDirPath = "/resources"; // Specify the resource directory path within the JAR
			// Get the JAR file containing the resources
			File jarFile = new File (this.getClass ().getProtectionDomain ().getCodeSource ().getLocation ().toURI ());
			JarFile jar = new JarFile (jarFile);

			Enumeration<JarEntry> entries = jar.entries (); // Get a list of resource file and directory names
			while (entries.hasMoreElements ()) {
				JarEntry entry = entries.nextElement ();
				String entryName = entry.getName ();

				if (entryName.startsWith ("resources")) {  // Check if the entry is in the specified resource directory
					Path destinationPath = Paths.get (docModel.temporalPath, "resources", entryName.substring (resourceDirPath.length ()));
					if (entry.isDirectory ())
						Files.createDirectories (destinationPath); // This is a directory, so create it in the destination
					else // This is a file, so copy it to the destination
						try (InputStream inputStream = jar.getInputStream (entry)) {
						Files.copy (inputStream, destinationPath, StandardCopyOption.REPLACE_EXISTING);
					}
				}
			}
			jar.close ();
		} catch (IOException | URISyntaxException ex) {
			System.out.println ("--- ERROR copiando recursos desde JAR");
			return false;
		}
		return true;
	}

	public boolean copyResourcesFromPathToTempDir () {
		try {
			String resourceDir = "resources/";// Specify the resource directory path within the JAR			
			ClassLoader classLoader = this.getClass ().getClassLoader ();// Get a reference to the current class loader			
			URL resourceUrl = classLoader.getResource (resourceDir);// Get the URL of the resource directory
			if (resourceUrl == null)
				System.out.println ("SERVER: Carpeta de recursos no encontrada: " + resourceDir);
			else {
				URI uri = resourceUrl.toURI ();
				Path resourcePath = Paths.get (uri);// Convert the URL to a Path		
				Files.walk (resourcePath)// Walk the directory and collect all resource names
					.forEach (filePath -> {
						if (filePath.equals (resourcePath) == false) {
							Path relativePath = resourcePath.relativize (filePath);
							Path destinationPath = Paths.get (docModel.temporalPath, resourceDir, relativePath.toString ());
							if (Files.isDirectory (destinationPath))
								destinationPath.toFile ().mkdir ();
							else
							try {
								Files.copy (filePath, destinationPath, StandardCopyOption.REPLACE_EXISTING);
							} catch (IOException ex) {
								Logger.getLogger (this.getClass ().getName ()).log (Level.SEVERE, null, ex);
							}
						}
					}
					);
			}
		} catch (URISyntaxException | IOException ex) {
			System.out.println ("--- ERROR copiando recursos desde TEMP");
			ex.printStackTrace ();
			return false;
		}
		return true;
	}

	public static void main (String[] args) {
		try {
			MainController ctr = new MainController ();
			ServerProcess rw = new ServerProcess (new Controller (), new DocModel ());
			//rw.execute ();
			new Thread(() -> rw.execute ()).start();

		} catch (Exception ex) {
			Logger.getLogger (ServerProcess.class
				.getName ()).log (Level.SEVERE, null, ex);
		}
	}
}
