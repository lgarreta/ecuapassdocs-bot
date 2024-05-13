import javax.swing.*;
import javax.swing.event.*;
import javax.swing.filechooser.*;
import javax.swing.filechooser.FileView;
import javax.swing.filechooser.FileSystemView;
import java.awt.*;
import java.awt.event.*;
import java.beans.*;
import java.io.*;


public class FileChooserDoubleClickExample {
    public static void main(String[] args) {
        JFrame frame = new JFrame("FileChooser Double Click Example");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
        
        fileChooser.setFileView(new FileView() {
            @Override
            public Icon getIcon(File f) {
                return FileSystemView.getFileSystemView().getSystemIcon(f);
            }
        });

        fileChooser.addPropertyChangeListener(new PropertyChangeListener() {
            @Override
            public void propertyChange(PropertyChangeEvent evt) {
                if (JFileChooser.SELECTED_FILE_CHANGED_PROPERTY.equals(evt.getPropertyName())) {
                    File selectedFile = fileChooser.getSelectedFile();
                    if (selectedFile != null) {
                        System.out.println("Selected file: " + selectedFile.getAbsolutePath());
                    }
                }
            }
        });

        JScrollPane scrollPane = findScrollPane(fileChooser);
        if (scrollPane != null) {
            JList fileList = (JList) scrollPane.getViewport().getView();
            fileList.addListSelectionListener(new ListSelectionListener() {
                @Override
                public void valueChanged(ListSelectionEvent e) {
                    if (!e.getValueIsAdjusting()) {
                        File selectedFile = (File) fileList.getSelectedValue();
                        if (selectedFile != null && e.getClickCount() == 2) {
                            if (selectedFile.isDirectory()) {
                                fileChooser.setCurrentDirectory(selectedFile);
                            } else {
                                System.out.println("Double-clicked on file: " + selectedFile.getAbsolutePath());
                            }
                        }
                    }
                }
            });
        }

        frame.add(fileChooser);
        frame.pack();
        frame.setVisible(true);
    }

    private static JScrollPane findScrollPane(Component component) {
        if (component instanceof JScrollPane) {
            return (JScrollPane) component;
        }
        if (component instanceof Container) {
            Component[] children = ((Container) component).getComponents();
            for (Component child : children) {
                JScrollPane scrollPane = findScrollPane(child);
                if (scrollPane != null) {
                    return scrollPane;
                }
            }
        }
        return null;
    }
}

