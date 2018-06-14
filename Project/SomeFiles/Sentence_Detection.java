package substitution_enron_fong;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;
import java.util.Vector;

public class Sentence_Detection {
	//private static BufferedReader reader1 = null;
	//static String sentence_examples = "/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/Sentences_in_Paragraphs.txt";
	static Vector<String> final_parsed_Sentences=new Vector<String>();
	static Vector<String> temp_parsed_Sentences=new Vector<String>();
	private static BufferedWriter writer_1 = null;
	static String sentence_in_file= "/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/Parsed_Enron_Sentences.txt";
	public static void main(String[] args) {
		try{
			FileInputStream fstream = new FileInputStream("/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/Sentences_in_Paragraphs.txt");
			BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

			//reader1 =  new BufferedReader(new FileReader(sentence_examples));
			writer_1 = new BufferedWriter(new FileWriter(sentence_in_file));
			String text = "";
			while (( text = br.readLine()) != null){
				text=text.trim();
				SentenceBoundaryDemo obj_sbd=new SentenceBoundaryDemo();
				//temp_parsed_Sentences=obj_sbd.Sentence_Chunker(text);
				final_parsed_Sentences.addAll(obj_sbd.Sentence_Chunker(text));
				}
			for(String s: final_parsed_Sentences){
				writer_1.append(s);
				writer_1.append("\n");
				
			}
			writer_1.flush();
			writer_1.close();
		
			}catch (IOException e) {
				e.printStackTrace();
				}
		}
	}
