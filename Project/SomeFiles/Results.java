package substitution_enron_fong;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.ObjectInputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.aliasi.hmm.HiddenMarkovModel;
import com.aliasi.hmm.HmmDecoder;
import com.aliasi.tokenizer.RegExTokenizerFactory;
import com.aliasi.tokenizer.Tokenizer;
import com.aliasi.tokenizer.TokenizerFactory;
import com.aliasi.util.Streams;
import com.cybozu.labs.langdetect.LangDetectException;

import edu.smu.tspell.wordnet.NounSynset;
import edu.smu.tspell.wordnet.Synset;
import edu.smu.tspell.wordnet.SynsetType;
import edu.smu.tspell.wordnet.WordNetDatabase;


public class Results {
	private static BufferedReader reader1 = null;
	static String profileDirectory = "/Users/agrawal/Desktop/BDA_ConceptNet/langdetect-03-03-2014/profiles";

	static String parsed_data = "/Users/agrawal/Desktop/brown_data.txt";
	private static BufferedWriter writer_1 = null;
	static String excel_sheet= "/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/brown_corpus.xls";
	static String bnc_noun_corpus = "/Users/agrawal/Desktop/BDA_ConceptNet/FrequencyList_Noun.txt";
	static List<String> tokenList=new ArrayList<String>();
	static List<String> bnc_noun_list=new ArrayList<String>();
	static List<String> bnc_noun_freq_list=new ArrayList<String>();
	static String big_corpus = "/Users/agrawal/Desktop/BDA_ConceptNet/Results_Substitution_Enron/100K_list_1.txt";
	static List<String> big_corpus_noun_list=new ArrayList<String>();
	static List<String> big_corpus_freq_list=new ArrayList<String>();
	public static void main(String[] args) {
		try{
		
			System.out.println("started");
			reader1 =  new BufferedReader(new FileReader(bnc_noun_corpus));
			Detect_Language dl=new Detect_Language();
			dl.init(profileDirectory);
			String text1 = "";
			while (( text1 = reader1.readLine()) != null){
				text1=text1.trim();
				int loc_tab=text1.lastIndexOf(" ");
				String bnc_noun_freq=text1.substring(loc_tab).replaceAll(" ", "");
				String bnc_noun=text1.substring(0, loc_tab);
				bnc_noun_list.add(bnc_noun);
				bnc_noun_freq_list.add(bnc_noun_freq);
				}
			text1="";
			reader1 =  new BufferedReader(new FileReader(big_corpus));
			while (( text1 = reader1.readLine()) != null){
				text1=text1.trim();
				int loc_tab=text1.lastIndexOf(" ");
				String bnc_noun_freq=text1.substring(loc_tab).replaceAll(" ", "");
				String bnc_noun=text1.substring(0, loc_tab);
				big_corpus_noun_list.add(bnc_noun);
				big_corpus_freq_list.add(bnc_noun_freq);
				}
			//System.out.println("big_corpus_freq_list: "+ big_corpus_freq_list.size());
			reader1 =  new BufferedReader(new FileReader(parsed_data));
			String text = "";
			writer_1 = new BufferedWriter(new FileWriter(excel_sheet));
			writer_1.append("Sentence" + "\t" + "is_5_15" + "\t" + "sentence_length" + "\t" + "first_noun" + "\t" + "is_in_bnc" + "\t" + "has_hypernym" + "\t" + "language_BNC" + "\t" + "in_big_corpus" + "\t" + "lanaguage_big_corpus" + "\t" + "java_language" + "\t" + "freq_BNC" + "\t" + "noun_dash_BNC" + "\t" + "freq_dash_BNC" + "\t" + "freq_Big" + "\t" + "noun_dash_big" + "\t" + "freq_dash_big" + "\t" + "sentence_dash_BNC" + "\t" + "sentence_dash_big");
			writer_1.append("\n");
			SentenceBoundaryDemo obj_sbd=new SentenceBoundaryDemo();
			
			while (( text = reader1.readLine()) != null){
				int is_fivefifteen=0, is_in_bnc=0, has_hypernym=0, in_big_corpus=0;
				int language=0, java_lan=1;
				String freq=null, noun_dash=null, freq_dash=null, sentence_dash=null;
				int language_big=0;
				String freq_big=null, noun_dash_big=null, freq_dash_big=null, sentence_dash_big=null;
				text=text.trim(); 
			
				// in every iteration text has one sentence from parsed data file.
				text=text.replace("\t", "");
				text=text.replace("!", "");
				text=text.replace("\t", " ");
				text=text.replaceAll("\\s+", " ");
				System.out.println("text done: " + text);
				@SuppressWarnings("static-access")
				String java_language=dl.detect(text);
				if(java_language.equalsIgnoreCase("en")){
					java_lan=1;
				}else{
					java_lan=0;
				}
			//	System.out.println("java lang: "+ java_lan);
				//CHECK SENTENCE LENGTH
				List<String> tokens=obj_sbd.sen_boundary(text);
				int sen_length=tokens.size();
				if(sen_length>4 && sen_length<16){
					is_fivefifteen=1;
					}else{
						is_fivefifteen=0;
					}
				//System.out.println("word length: "+ sen_length);
				String first_noun=Find_First_Noun(text);
			//	System.out.println("first noun: " + first_noun);
				if(first_noun==null){
					is_in_bnc=0;
					has_hypernym=0;
					language=0;
					in_big_corpus=0;
					first_noun="-";
				}else{
				boolean decision= bnc_noun_list.contains(first_noun);
				boolean decision_big_corpus=big_corpus_noun_list.contains(first_noun);
				//System.out.println("for sentence" + text + "presence of first noun in BNC: " + decision);
				//System.out.println("bnc list: " + decision);
			//	System.out.println("big corpus list: " + decision_big_corpus);

				boolean h_decision=hasHypernym_Wordnet(first_noun);
			//	System.out.println("hypernym: " + h_decision);
				if(h_decision){
					has_hypernym=1;
				}else{
					has_hypernym=0;
				}
				if(decision){
					is_in_bnc=1;
					}else{
					is_in_bnc=0;
					}

				if(decision_big_corpus){
					in_big_corpus=1;
				}else{
					in_big_corpus=0;
				}
				}
			

				//System.out.println("final values of inbnc n hashypernym");
				int new_loc=0;
				if(is_in_bnc==1 && has_hypernym==1){

					language=1;
					int loc_noun_in_bnc=bnc_noun_list.indexOf(first_noun);
					freq=bnc_noun_freq_list.get(loc_noun_in_bnc);
					
					//System.out.println(freq + "\t" + loc_noun_in_bnc);
					if(loc_noun_in_bnc>1){
					new_loc=loc_noun_in_bnc-1;
					
					}else{
						new_loc=loc_noun_in_bnc+1;
					}
					// make sure entries in corpus are sorted (decreasing order).
				
					//System.out.println(bnc_noun_list.get(new_loc));
					noun_dash=bnc_noun_list.get(new_loc);
					freq_dash=bnc_noun_freq_list.get(new_loc);
					sentence_dash=text.replaceFirst(first_noun, noun_dash);
					
				}else{

					language=0;
					freq="-";
					noun_dash="-";
					freq_dash="-";
					sentence_dash="-";
				}
				if(in_big_corpus==1&&has_hypernym==1){
					language_big=1;
					int loc_noun_in_big=big_corpus_noun_list.indexOf(first_noun);
					freq_big=big_corpus_freq_list.get(loc_noun_in_big);
					if(loc_noun_in_big>1){
					new_loc=loc_noun_in_big-1;
					}else{
						new_loc=loc_noun_in_big+1;;
					}
					// make sure entries in corpus are sorted (decreasing order).
					noun_dash_big=big_corpus_noun_list.get(new_loc);
					freq_dash_big=big_corpus_freq_list.get(new_loc);
					sentence_dash_big=text.replaceFirst(first_noun, noun_dash_big);
				}else{

					language_big=0;
					freq_big="-";
					noun_dash_big="-";
					freq_dash_big="-";
					sentence_dash_big="-";
				}
				

				//System.out.println(text + "\t" + is_fivefifteen + "\t" + first_noun + "\t" + is_in_bnc + "\t" + has_hypernym);
				writer_1.append(text + "\t" + is_fivefifteen + "\t" + sen_length + "\t" + first_noun + "\t" + is_in_bnc + "\t" + has_hypernym + "\t" + language + "\t" + in_big_corpus + "\t" + language_big + "\t" + java_lan + "\t" + freq + "\t" + noun_dash + "\t" + freq_dash + "\t" + freq_big + "\t" + noun_dash_big + "\t" + freq_dash_big + "\t" + sentence_dash + "\t" + sentence_dash_big);
				writer_1.append("\n");
				}
			writer_1.flush();
			writer_1.close();
			System.out.println("completed");
			
		}catch(Exception e){
			e.getStackTrace();
		}
		

	}

private static boolean hasHypernym_Wordnet(String first_Noun) {
		NounSynset nounSynset; 
		NounSynset[] hypernyms = null; 

		WordNetDatabase database = WordNetDatabase.getFileInstance(); 
		Synset[] synsets = database.getSynsets(first_Noun, SynsetType.NOUN);
		//System.out.println("synsets length: "+ synsets.length);
		int synset_length=synsets.length;
		boolean result;
		if(synset_length>0){
		for (int i = 0; i < synset_length; i++) { 
			//System.out.println(synsets[i]);
			// System.out.println("hello before nounsynset");
		    nounSynset = (NounSynset)(synsets[i]); 
		    //System.out.println("hello after nounsynset");
		    hypernyms = nounSynset.getHypernyms();
		    //System.err.println(nounSynset.getWordForms()[0] + ": " + nounSynset.getDefinition() + ") has " + hypernyms.length + " hyponyms");
		    }
		if(hypernyms.length>0){
			result=true;
		}else{
			//System.out.println(first_Noun);
			result=false;
		}
		
	}else{
		result=false;
	}
		
		
		return result;

	}

	private static String Find_First_Noun(String text_new) {
		String first_noun=null;
		try{
			String filename = "./pos-en-general-brown.HiddenMarkovModel";
			//System.out.println("Reading model from file=" + filename);
			FileInputStream fileIn = new FileInputStream(filename);
			ObjectInputStream objIn = new ObjectInputStream(fileIn);
			HiddenMarkovModel hmm = (HiddenMarkovModel) objIn.readObject();
			Streams.closeQuietly(objIn);
			HmmDecoder decoder = new HmmDecoder(hmm);
			TokenizerFactory TOKENIZER_FACTORY = new RegExTokenizerFactory("(-|'|\\d|\\p{L})+|\\S");	
			char[] cs = text_new.toCharArray();
			Tokenizer tokenizer = TOKENIZER_FACTORY.tokenizer(cs, 0, cs.length);
			String[] tokens = tokenizer.tokenize();
			tokenList = Arrays.asList(tokens);
			List<String> tags= RunMedPost.firstBest(tokenList, decoder);
			for(String s: tags){
				if(s.equals("nn")||s.equals("np")||s.equals("nr")){
					int loc=tags.indexOf(s);
					first_noun=tokenList.get(loc);
					break;
				}
			}
			}catch(Exception e){
				e.getStackTrace();
				}
		return first_noun;
		}
	}
