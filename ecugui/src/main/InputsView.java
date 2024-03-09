package main;

import documento.DocRecord;
import java.awt.Component;
import java.awt.Desktop;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.net.URI;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFileChooser;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JViewport;
import javax.swing.Timer;
import javax.swing.UIManager;
import javax.swing.filechooser.FileNameExtensionFilter;
import widgets.ImageViewLens;
import widgets.InputsControlPanel;

public class InputsView extends javax.swing.JPanel {

	@SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    filesPanel = new javax.swing.JPanel();
    selectionPanel = new javax.swing.JPanel();
    fileChooser = new javax.swing.JFileChooser();
    controlsPanel = new widgets.InputsControlPanel();
    jPanel1 = new javax.swing.JPanel();
    buttonOpenEcuapassdocs = new javax.swing.JButton();
    buttonProcessSelection = new javax.swing.JButton();
    buttonOpenEcuapass = new javax.swing.JButton();
    filesTable = new main.FileSelectionTable();
    imageView = new widgets.ImageViewLens();

    setLayout(new java.awt.BorderLayout());

    filesPanel.setLayout(new javax.swing.BoxLayout(filesPanel, javax.swing.BoxLayout.Y_AXIS));

    selectionPanel.setPreferredSize(new java.awt.Dimension(580, 700));
    selectionPanel.setLayout(new java.awt.BorderLayout());

    fileChooser.setBackground(new java.awt.Color(204, 255, 204));
    fileChooser.setControlButtonsAreShown(false);
    fileChooser.setAlignmentY(0.1F);
    fileChooser.setAutoscrolls(true);
    fileChooser.setBorder(javax.swing.BorderFactory.createTitledBorder("Selección de facturas:"));
    fileChooser.setMinimumSize(new java.awt.Dimension(442, 200));
    fileChooser.setMultiSelectionEnabled(true);
    selectionPanel.add(fileChooser, java.awt.BorderLayout.CENTER);

    controlsPanel.setBackground(new java.awt.Color(204, 255, 204));
    selectionPanel.add(controlsPanel, java.awt.BorderLayout.PAGE_END);

    jPanel1.setBackground(new java.awt.Color(204, 255, 204));
    jPanel1.setBorder(javax.swing.BorderFactory.createTitledBorder("Un sólo documento:"));

    buttonOpenEcuapassdocs.setText("<html>Crear<br>Documentos</html>");
    buttonOpenEcuapassdocs.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(java.awt.event.ActionEvent evt) {
        buttonOpenEcuapassdocsActionPerformed(evt);
      }
    });
    jPanel1.add(buttonOpenEcuapassdocs);

    buttonProcessSelection.setText("<html>  Procesar <br>  Selección  </html>");
    buttonProcessSelection.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(java.awt.event.ActionEvent evt) {
        buttonProcessSelectionActionPerformed(evt);
      }
    });
    jPanel1.add(buttonProcessSelection);

    buttonOpenEcuapass.setText("<html> Ingresar <br> ECUAPASS </html>");
    buttonOpenEcuapass.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(java.awt.event.ActionEvent evt) {
        buttonOpenEcuapassActionPerformed(evt);
      }
    });
    jPanel1.add(buttonOpenEcuapass);

    selectionPanel.add(jPanel1, java.awt.BorderLayout.PAGE_START);

    filesPanel.add(selectionPanel);
    filesPanel.add(filesTable);

    add(filesPanel, java.awt.BorderLayout.WEST);
    add(imageView, java.awt.BorderLayout.CENTER);
  }// </editor-fold>//GEN-END:initComponents

  private void buttonOpenEcuapassdocsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonOpenEcuapassdocsActionPerformed
		// TODO add your handling code here
		controller.openCreadorDocumentosEcuapass ();
		/*
		String url = "https://ecuapassdocs-production.up.railway.app/"; // Specify the URL here

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
		*/
  }//GEN-LAST:event_buttonOpenEcuapassdocsActionPerformed

  private void buttonProcessSelectionActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonProcessSelectionActionPerformed
		// TODO add your handling code here:
		controller.onReinitialize ();		
		// Send filechooser file to selected files in table
		try {
			controller.onSendSelectedFiles ();
			controller.onStartProcessing ();
		} catch (FileNotFoundException ex) {
			Logger.getLogger (InputsControlPanel.class.getName ()).log (Level.SEVERE, null, ex);
		}

  }//GEN-LAST:event_buttonProcessSelectionActionPerformed

  private void buttonOpenEcuapassActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonOpenEcuapassActionPerformed
		// TODO add your handling code here:
  }//GEN-LAST:event_buttonOpenEcuapassActionPerformed

  // Variables declaration - do not modify//GEN-BEGIN:variables
  private javax.swing.JButton buttonOpenEcuapass;
  private javax.swing.JButton buttonOpenEcuapassdocs;
  private javax.swing.JButton buttonProcessSelection;
  private widgets.InputsControlPanel controlsPanel;
  private javax.swing.JFileChooser fileChooser;
  private javax.swing.JPanel filesPanel;
  private main.FileSelectionTable filesTable;
  private widgets.ImageViewLens imageView;
  private javax.swing.JPanel jPanel1;
  private javax.swing.JPanel selectionPanel;
  // End of variables declaration//GEN-END:variables

	Controller controller;

	public InputsView () {
		initComponents ();
		modifyFileChooser ();
		this.controlsPanel.setVisible (false);
		this.filesTable.setVisible (false);
	}

	public void setController (Controller controller) {
		this.controller = controller;
		filesTable.setController (controller, "tableSelectedFiles");
		//filesTable.setDoctypeComboBoxToTable ();
		controlsPanel.setController (controller);
		addFileChooserListeners ();
	}

	public void addFileChooserListeners () {
		// Add listener for file selection (for preview)
		fileChooser.addPropertyChangeListener (new PropertyChangeListener () {
			@Override
			public void propertyChange (PropertyChangeEvent evt) {
				if (JFileChooser.SELECTED_FILE_CHANGED_PROPERTY.equals (evt.getPropertyName ())) {
					File selectedFile = fileChooser.getSelectedFile ();
					if (selectedFile != null && !selectedFile.isDirectory ())
						controller.onFileSelected (fileChooser.getSelectedFile ());
				}
			}
		});

		// Add a timer to refres dir content
		Timer timer = new Timer (5000, new ActionListener () { // Update every 5 seconds
			@Override
			public void actionPerformed (ActionEvent e) {
				fileChooser.rescanCurrentDirectory ();
			}
		});
		timer.start ();
	}

	private static JList getFileList (JFileChooser fileChooser) {
		Component[] components = fileChooser.getComponents ();
		for (Component component : components) {
			if (component instanceof JScrollPane) {
				JScrollPane scrollPane = (JScrollPane) component;
				JViewport viewport = scrollPane.getViewport ();
				Component[] viewportComponents = viewport.getComponents ();
				for (Component c : viewportComponents) {
					if (c instanceof JList)
						return (JList) c;
				}
			}
		}
		return null;
	}

private void modifyFileChooser () {
		// Changes FileChooser text from english to spanish 
		UIManager.put ("FileChooser.fileNameLabelText", "Archivos");
		UIManager.put ("FileChooser.filesOfTypeLabelText", "Tipos de Archivos");
		UIManager.put ("FileChooser.cancelButtonText", "Deseleccionar ");
		UIManager.put ("FileChooser.openButtonText", "Seleccionar ");
		UIManager.put ("FileChooser.lookInLabelText", "Buscar");

		UIManager.put ("FileChooser.readOnly", Boolean.TRUE);
		fileChooser.updateUI ();

		// Show only images and pdfs  in FileChooser
		fileChooser.setAcceptAllFileFilterUsed (false);
		FileNameExtensionFilter filter = new FileNameExtensionFilter ("Images/pdf files", "jpg", "png", "pdf");
		fileChooser.addChoosableFileFilter (filter);

		// Hide default accept/cancel buttons
		hideFileSelComponents (fileChooser.getComponents ());

	}

	// Hide last file panel from JFileChooser component
	private void hideFileSelComponents (Component[] components) {
		// traverse through the components
		for (int i = 0; i < components.length; i++) {
			Component comp = components[i];
			if (comp instanceof JPanel) // traverse recursively
				hideFileSelComponents (((JPanel) comp).getComponents ());
			else if (comp.toString ().contains ("Archivos"))
				comp.getParent ().getParent ().setVisible (false); // hide i
		}
	}

	public ImageViewLens getImageView () {
		return (imageView);
	}

	// Set FileChooser to selectedDir
	public void setSelectedDir (String selectedDir) {
		fileChooser.setCurrentDirectory (new File (selectedDir));
	}

	public File getFileAt (int row, int col) {
		return (new File (filesTable.getFileAt (row, col)));
	}

	public File[] getSelectedFiles () {
		File[] selectedFiles = fileChooser.getSelectedFiles ();
		for (File fi : selectedFiles) {
			System.out.println (fi.toString ());
		}
		return (selectedFiles);
	}

	public void selectAllFiles () {
		File[] allFiles = this.getAllFilesFromChooser ();
		//int fileCount = fileChooser.getCurrentDirectory ().listFiles ().length;
		//File[] allFiles = fileChooser.getCurrentDirectory ().listFiles ();
		fileChooser.setSelectedFiles (allFiles);
	}

	public File[] getAllFilesFromChooser () {
		fileChooser.setAcceptAllFileFilterUsed (false);
		FileNameExtensionFilter filter = new FileNameExtensionFilter ("Images/pdf files", "jpg", "png", "pdf");
		fileChooser.addChoosableFileFilter (filter);
		File wd = fileChooser.getCurrentDirectory ();

		java.io.FileFilter ioFilter = file -> filter.accept (file);
		File[] allFiles = wd.listFiles (ioFilter);

		return (allFiles);
	}

	public void addNoProcessedRecords (DocRecord record) {
		filesTable.addNoProcessedRecord (record);
	}

	// Remove record (map and table) give the doc filename
	public void removeRecord (String docFilename) {
		filesTable.removeRecord (docFilename);
	}

	public void clearSelectedFiles () {
		filesTable.clear ();
		File[] selFiles = fileChooser.getSelectedFiles ();
		if (selFiles.length == 1)
			return;

		File[] allFiles = this.getAllFilesFromChooser ();
		File[] noFiles = Arrays.copyOfRange (allFiles, 0, 1);
		File selFile = fileChooser.getSelectedFile ();
		if (noFiles.length > 0)
			fileChooser.setSelectedFiles (noFiles);
	}

	public void enableProcessingButton (boolean value) {
		controlsPanel.enableProcessingButton (value);
	}

	// Get documents from table and assign the document type
	boolean prepareRecords () {
		int nRows = filesTable.tableModel.getRowCount ();
		if (nRows == 0) {
			JOptionPane.showMessageDialog (this, "No hay documentos seleccionados para procesar!");
			return false;
		}

		for (int i = 0; i < nRows; i++) {
			String docName = (String) filesTable.getTable ().getValueAt (i, 1);
			DocRecord docRecord = (DocRecord) filesTable.recordsMap.get (docName);

			if (docRecord.docType.matches ("cartaporte|manifiesto|declaracion")) {
				filesTable.tableModel.setValueAt (docRecord.docType, i, 0);
				continue;
			} else {
				String docTypeTable = (String) filesTable.getTable ().getValueAt (i, 0);
				if (docTypeTable.matches ("CARTAPORTE|MANIFIESTO|DECLARACION")) {
					docRecord.setDocType (docTypeTable);
					continue;
				} else {
					JOptionPane.showMessageDialog (this, "Falta definir el tipo de documento: cartaporte, manifiesto o declaración");
					return false;
				}
			}
		}
		return true;
	}
}
