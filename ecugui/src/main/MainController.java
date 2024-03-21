package main;

import widgets.FeedbackView;
import documento.DocModel;
import documento.DocRecord;
import documento.SettingsController;
import java.awt.Desktop;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import widgets.ImageViewLens;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URI;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.UIManager;
import org.json.simple.parser.ParseException;
import results.ResultsController;
import widgets.ProgressDialog;
import workers.ServerWorker;

public class MainController extends Controller {

	String appRelease = "0.990";
	DocModel doc;             // Handles invoice data: selected, processed, and no procesed
	MainView mainView;
	InputsView inputsView;
	JTabbedPane tabsPanel;
	FeedbackView feedbackView;
	ImageViewLens imageView;
	//ResultsView resultsView;
	ResultsController resultsController;
	ServerWorker serverWorker;          // Client for sending messages to python server
	ProgressDialog progressDialog;     // Dialog showed when document processing starts
	
	SettingsController settingsController; // Initial configuration parameters

	public MainController () {
		try {
			doc = new DocModel ();
			doc.initGlobalPaths ();
			serverWorker = new ServerWorker (this, doc);
			initializeComponents ();
		} catch (Exception ex) {
			ex.printStackTrace ();
			Logger.getLogger (MainController.class.getName ()).log (Level.SEVERE, null, ex);
		}
		out ("Ecuapass-docs  " + appRelease);
	}

	public JFrame getMainView () {
		return mainView;
	}

	// Add the views to this Frame
	private void initializeComponents () {
		// Main views
		mainView = new MainView ();
		mainView.setController (this);
		mainView.setVisible (true);
		
		// Inital configuration dialog
		settingsController = new SettingsController (mainView, doc.companiesString, doc.runningPath);
		doc.companyName = settingsController.initCurrentWorkingCompany ();
		

		inputsView = new InputsView ();
		inputsView.setController (this);

		feedbackView = new FeedbackView ();
		feedbackView.setController (this, settingsController);


		tabsPanel = mainView.createTabs ();
		tabsPanel.addTab ("Entradas:", inputsView);
		tabsPanel.addTab ("Mensajes", feedbackView);

		// Get components from views
		imageView = inputsView.getImageView ();

		// Initialize dirs
		String location = AppPrefs.FileLocation.get (System.getProperty ("user.home"));
		inputsView.setSelectedDir (location);

		doc.printGlobalPaths (this);

		serverWorker.execute ();
	}

	// Start document processing after button pressed in InpusView
	@Override
	public void onStartProcessing () {
		// Check if document type was asigned
		if (inputsView.prepareRecords () == false)
			return;

		out ("Inicio del procesamiento de los documentos...");
		// Start resultsController
		if (resultsController != null)
			tabsPanel.remove (resultsController.resultsView);

		resultsController = new ResultsController (this, doc, serverWorker);
		tabsPanel.addTab ("Resultados", resultsController.resultsView);

		// Call to server to start processing documents
		serverWorker.copyDocsToWorkingDir (doc.getSelectedRecords ());
		serverWorker.startProcess ("doc_processing", doc.workingPath, DocModel.runningPath);
		progressDialog = new ProgressDialog (mainView);
		progressDialog.startProcess ();
	}

	@Override
	public void onTableCellSelected (int row, int col, String id) {
		File docFilepath = inputsView.getFileAt (row, col);
		onFileSelected (docFilepath);
	}

	// Selected docFile in  FileChooser or table from InputsFilesViewProjects
	@Override
	public void onFileSelected (File docFilepath) {
		imageView.showImage (docFilepath);
	}

	// Select all files from FileChooser
	@Override
	public void onSelectAllFiles () {
		inputsView.selectAllFiles ();
	}

	// InputsView files selected by FileChooser
	// Send selected file to ready table
	@Override
	public void onSendSelectedFiles () throws FileNotFoundException {
		out ("Alistando documentos seleccionados...");
		File[] selectedFiles = inputsView.getSelectedFiles ();
		if (selectedFiles.length > 0) {
			for (File docFilepath : selectedFiles) {
				DocRecord record = new DocRecord (docFilepath.toString ());
				if (doc.existsRecord (record) == false) {
					inputsView.addNoProcessedRecords (record);
					doc.addSelectedRecord (record);
				}
			}
			AppPrefs.FileLocation.put (selectedFiles[0].getParentFile ().getAbsolutePath ());
		} else
			JOptionPane.showMessageDialog (inputsView, "No hay documentos seleccionados!");
	}

	// ServeWorker notification 
	@Override
	public void onEndProcessing (String docFilepath, String msgStatus) {
		try {
			if (msgStatus.contains ("EXITO")) {
				String jsonFilepath = Utils.getResultsFile (docFilepath, "ECUFIELDS.json");
				String docType = new File (docFilepath).getName ().split ("-")[0];
				DocRecord record = new DocRecord (docType, docFilepath, jsonFilepath);
				doc.addProcessedRecord (record);
				resultsController.addProcessedRecord (record);
				resultsController.resultsView.selectFirstRecord ();
				progressDialog.endProcess ("document_processed");
				inputsView.removeRecord (record.docFilename);
			} else {
				out (docFilepath + " procesado con errores");
				doc.addNotProcessedFile (docFilepath);
			}
			tabsPanel.setSelectedIndex (2);
		} catch (ParseException | IOException ex) {
			Logger.getLogger (MainController.class.getName ()).log (Level.SEVERE, null, ex);
		}
	}

	// Worker notification for adding processed file to 'resultsController' 
	@Override
	public void onProcessDocumentsEndAll () {
		out ("Procesados con éxito todos los documentos.");
	}

	// Stop cartaporte server if it was opened
	@Override
	public void onWindowClossing () {
		try {
			boolean stopFlag = serverWorker.startProcess ("stop", null, null);
			out ("Finalizando servidor cartaportes." + stopFlag);
			System.exit (0);
		} catch (Exception ex) {
			System.exit (0);
		}
	}

	//  InputsFileView for "reinitialize" selection
	@Override
	public void onReinitialize () {
		inputsView.clearSelectedFiles ();
		doc.removeAllFiles ();
	}

	// Write message text to both: stdout and FeedbackView
	@Override
	public void out (String s
	) {
		s = "> " + s;
		System.out.println (s);
		feedbackView.println (s);
	}

	@Override
	public void setWindowState (String state
	) {
		if (state.equals ("minimize"))
			mainView.setState (JFrame.ICONIFIED);
		else if (state.equals ("restore"))
			mainView.setState (JFrame.NORMAL);
	}

	@Override
	public void onServerRunning (int urlPortNumber
	) {
		out ("Cliente java escuchando en el puerto: " + urlPortNumber);
		inputsView.enableProcessingButton (true);
	}

	// Send feedback to cloud
	@Override
	public void onSendFeedback (String docFilepath) {
		String feedbackText = feedbackView.getFeedbackText ();
		String zipFilepath = Utils.createTempCompressedFileFromText (feedbackText);
		// Call to server to start processing documents
		serverWorker.startProcess ("send_feedback", zipFilepath, docFilepath);
	}

	public String getAppRelease () {
		return this.appRelease;
	}

	public void onWorkingCountrySelected (String workingCountry) {
		System.out.println ("Country Selected: " + workingCountry);
	}

	// First time initialization. Set "empresa" name for  cloud document models
	void initCurrentWorkingCompany () {
		try {
			File settingsFile = new File (doc.runningPath + "/settings.txt");
			if (settingsFile.exists ()) {// Load comany name
				BufferedReader reader = new BufferedReader (new FileReader (settingsFile));
				doc.companyName = reader.readLine ();
			} else { // Request company name
				JTextField textField = new JTextField ();
				Object[] message = {"Nombre de la empresa:", textField};
				Object[] options = {"Aceptar", "Cancelar"};
				while (true) {
					int option = JOptionPane.showOptionDialog (mainView, message, "Configuración Inicial de la Empresa",
						JOptionPane.DEFAULT_OPTION, JOptionPane.INFORMATION_MESSAGE, null, options, null);

					if (option == JOptionPane.OK_OPTION) {
						doc.companyName = textField.getText ().toUpperCase ();
						if (doc.companyName.matches (doc.companiesString)) {
							BufferedWriter writer = new BufferedWriter (new FileWriter (settingsFile, true));
							writer.write (doc.companyName);
							writer.close ();
							break;
						}
					} else
						System.exit (0);
				}
			}
			out (">>>>>>>>> Empresa: " + doc.companyName + " <<<<<<<<<<");
		} catch (Exception ex) {
			ex.printStackTrace ();
		}
	}
	
  public void openCreadorDocumentosEcuapass () {             
		String url = this.settingsController.getValue ("url_creador");
		try {
			// Check if the Desktop API is supported (available on desktop environments)
			if (Desktop.isDesktopSupported ()) {
				// Get the desktop object
				Desktop desktop = Desktop.getDesktop ();

				// Open the specified URL in the default browser
				desktop.browse (new URI (url));
			} else
				System.out.println ("Desktop API is not supported on this platform.");
		} catch (Exception e) {
			e.printStackTrace ();
		}
  }                                                      
	

	public static void main (String args[]) {

		//Set the Nimbus look and feel
		//<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
		/*
		 * If Nimbus (introduced in Java SE 6) is not available, stay with the
		 * default look and feel. For details see
		 * http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html
		 */
		try {
			for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels ()) {
				UIManager.setLookAndFeel (UIManager.getCrossPlatformLookAndFeelClassName ());
				//if ("Nimbus".equals (info.getName ())) {
				//	javax.swing.UIManager.setLookAndFeel (info.getClassName ());
				//	break;
				//}
			}
		} catch (ClassNotFoundException | InstantiationException | IllegalAccessException | javax.swing.UnsupportedLookAndFeelException ex) {
			java.util.logging.Logger.getLogger (MainView.class.getName ()).log (java.util.logging.Level.SEVERE, null, ex);
		}
		//</editor-fold>

		//</editor-fold>
		//  Create and display the form
		java.awt.EventQueue.invokeLater (new Runnable () {
			public void run () {
				new MainController ();
			}
		});

	}
}
