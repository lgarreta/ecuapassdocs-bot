package results;

import documento.DocModel;
import documento.DocRecord;
import widgets.ImageViewLens;
import main.Controller;
import main.FileSelectionTable;
import main.Utils;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import workers.ServerWorker;

public class ResultsController extends Controller {

	Controller controller;
	DocModel docModel;

	public ResultsView resultsView;
	FileSelectionTable fileSelectionTable;
	EcuapassView ecuapassView;
	ImageViewLens imageView;
	ServerWorker serverWorker;  // Server listening messages and executing tasks

	public ResultsController (Controller controller, DocModel docModel, ServerWorker serverWorker) {
		this.controller = controller;
		this.docModel = docModel;
		this.serverWorker = serverWorker;

		resultsView = new ResultsView ();
		resultsView.setController (this);
		imageView = resultsView.getImageView ();
		fileSelectionTable = resultsView.getFileSelectionTable ();
		fileSelectionTable.disableEdition ();
	}

	public ResultsController (Controller controller, DocModel model, ResultsView resultsview) {
		this.controller = controller;
		this.docModel = model;
		this.resultsView = resultsview;

		imageView = resultsView.getImageView ();
	}

	@Override
	public JFrame getMainView () {
		return controller.getMainView ();
	}

	// Fired from TablePanel when selected a record
	@Override
	public void onTableCellSelected (int row, int col, String id) {
		DocRecord record = null;
		if (id.equals ("tableProcessedFiles")) {
			record = fileSelectionTable.getRecordAt (row);
			showRecord (record);
		}
		if (id.equals ("simpleTableProcessedFiles")) {
			record = fileSelectionTable.getRecordAt (row);
			showRecord (record);
		}
	}

	// Show document image and record into ResultsView
	public void showRecord (DocRecord docRecord) {
		try {
			imageView.showImage (new File (docRecord.docFilepath));
			if (docRecord.docType.equals ("cartaporte"))
				ecuapassView = new EcuapassViewCartaporte ();
			else if (docRecord.docType.equals ("manifiesto"))
				ecuapassView = new EcuapassViewManifiesto ();
			else if (docRecord.docType.equals ("declaracion"))
				ecuapassView = new EcuapassViewDeclaracion ();

			resultsView.setRecordView (ecuapassView);
			ecuapassView.setRecord (docRecord);
			ecuapassView.showRecord ();
		} catch (Exception ex) {
			Logger.getLogger (ResultsController.class.getName ()).log (Level.SEVERE, null, ex);
		}
	}

	public void addProcessedRecord (DocRecord record) {
		fileSelectionTable.addProcessedRecord (record);
	}

	// Processing button pressed in InpusView
	@Override
	public void onBotSubmitToEcuapass () {
		out ("Inicio de digitación automatica del documento...");
		if (docModel.getSelectedRecords ().isEmpty ()) {
			JOptionPane.showMessageDialog (null, "No hay documentos seleccionadoss para procesar!");
			return;
		}
		// Get selected document and update it
		String docFilename = fileSelectionTable.getCurrentFileSelected ();
		String jsonFilename = Utils.getResultsFile (docFilename, "ECUFIELDS.json");
		this.updateJsonDocumentWithViewChanges (docModel.workingPath, jsonFilename);
		//controller.setWindowState ("minimize");
		// Send message to server to process selected file
		//if (Win32.activateMaximizeEcuapassWindow ())
		serverWorker.startProcess ("bot_processing", jsonFilename, docModel.runningPath);
	}

	@Override
	public void onBotSubmitToCodebin () {
		out ("Transmistiendo el documento al CODEBIN...");
		if (docModel.getSelectedRecords ().isEmpty ()) {
			JOptionPane.showMessageDialog (null, "No hay documentos seleccionadoss para transmitir!");
			return;
		}
		// Get selected document and update it
		String docFilename = fileSelectionTable.getCurrentFileSelected ();
		String jsonFilename = Utils.getResultsFile (docFilename, "BINFIELDS.json");
		serverWorker.startProcess ("codebin_processing", jsonFilename, docModel.runningPath);
	}

	public void updateJsonDocumentWithViewChanges (String workingDir, String jsonFilename) {
		DocRecord docRecord = ecuapassView.updateRecord ();
		String jsonFilepath = Paths.get (workingDir, jsonFilename).toString ();
		docRecord.writeToJsonFile (jsonFilepath);
	}

	// RunWorker notification
	public void onProcessingEnd (String docFilepath, String msgStatus) {
		out (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
		if (msgStatus.contains ("success"))
			out (docFilepath + " ingresada con éxito");
		else
			out (docFilepath + " ingresada con errores");
		out (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
	}

	void writeStringToFile (String text, File outFilepath) {
		try {
			FileWriter csvWriter = new FileWriter (outFilepath);
			csvWriter.append (text);
			csvWriter.close ();

		} catch (IOException ex) {
			Logger.getLogger (ResultsController.class
				.getName ()).log (Level.SEVERE, null, ex);
		}
	}

	// Get the results (JSON) filename from doc filename (PNG)
//	public File getResultsFile (File docFilepath) {
//		controller.out ("Getting results file from: " + docFilepath);
//		String[] splitPath = docFilepath.getName ().split ("\\.(?=[^\\.]+$)");
//		String invoiceFilename = splitPath[0];
//		String workingDir = docModel.workingPath;
//		String resultsFilename = String.format ("%s-RESULTS-VALUES.json", invoiceFilename);
//		File resultsFilepath = new File (workingDir, resultsFilename);
//		return (resultsFilepath);
//	}
	public void out (String text) {
		controller.out (text);
	}
}
