package substitution_enron_fong;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.HashSet;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Enron_Mail_Parsing {
	private static BufferedReader br = null;
	private static BufferedWriter writer_1 = null;
	static String sentence_paragraphs = "/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/Sentences_in_Paragraphs_1.txt";
	static Vector<String> final_parsed_Sentences=new Vector<String>();

	public static void main(String[] args) {
			String path="/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/Enron_Data_Arnold/";
			try{
				writer_1 = new BufferedWriter(new FileWriter(sentence_paragraphs));
				File directory = new File(path);
				File[] files = directory.listFiles();
				String line = null;
				//System.out.println(files.length);
				for(int i=0;i<files.length;i++) {
					String sentence_para="";
				//System.out.println("reading "+i+ " file");
					FileReader fr = new FileReader(files[i]);
					br = new BufferedReader(fr);
					//writer_1.append(files[i].toString());
				//	writer_1.append("\n");
					//System.out.println(files[i]);
					final_parsed_Sentences.clear();
					while((line=br.readLine())!=null) {
						if(line.indexOf("Message-ID:")==0||line.indexOf("Date")==0||line.indexOf("From:")==0||line.indexOf("To:")==0||line.indexOf("Subject:")==0||line.indexOf("Cc:")==0||line.indexOf("Mime-Version:")==0||line.indexOf("Content-Type:")==0||line.indexOf("Content-Transfer-Encoding:")==0||line.indexOf("Bcc:")==0||line.indexOf("X-From:")==0||line.indexOf("X-To:")==0||line.indexOf("X-cc:")==0||line.indexOf("X-bcc:")==0||line.indexOf("X-Folder:")==0||line.indexOf("X-Origin:")==0||line.indexOf("X-FileName:")==0||line.indexOf("cc:")==0){
							//do nothing.
							}else{
								
								line=line.trim();
								
								sentence_para+=line;
								sentence_para+=" ";
								
								}
						}
					sentence_para=sentence_para.replaceAll("\\s+", " ");
					SentenceBoundaryDemo obj_sbd=new SentenceBoundaryDemo();
					//temp_parsed_Sentences=obj_sbd.Sentence_Chunker(text);
					final_parsed_Sentences.addAll(obj_sbd.Sentence_Chunker(sentence_para));
					HashSet hs = new HashSet();
					hs.addAll(final_parsed_Sentences);
					final_parsed_Sentences.clear();
					final_parsed_Sentences.addAll(hs);
					Pattern re = Pattern.compile("[^.!?\\s][^.!?]*(?:[.!?](?!['\"]?\\s|$)[^.!?]*)*[.!?]?['\"]?(?=\\s|$)", Pattern.MULTILINE | Pattern.COMMENTS);
					
				for(String s: final_parsed_Sentences){
					//writer_1.append(s);
					//writer_1.append("\n");
					Matcher reMatcher = re.matcher(s);
					while (reMatcher.find()) {
						//System.out.println(reMatcher.group());
						writer_1.append(reMatcher.group());
						writer_1.append("\n");
					}
					      
							//writer_1.append("\n");
					    //}
					
				}
					//Pattern re = Pattern.compile("[^.!?\\s][^.!?]*(?:[.!?](?!['\"]?\\s|$)[^.!?]*)*[.!?]?['\"]?(?=\\s|$)", Pattern.MULTILINE | Pattern.COMMENTS);
				   // Matcher reMatcher = re.matcher(sentence_para);
				   // while (reMatcher.find()) {
					
				        //System.out.println(reMatcher.group());
				        //writer_1.append(reMatcher.group());
						//writer_1.append("\n");
				    //}
					//writer_1.append(sentence_para);
					//writer_1.append("\n");
				
					}
				br.close();
				writer_1.flush();
				writer_1.close();
				}catch(Exception e){
					System.out.println(e);
					}
			}
	}

