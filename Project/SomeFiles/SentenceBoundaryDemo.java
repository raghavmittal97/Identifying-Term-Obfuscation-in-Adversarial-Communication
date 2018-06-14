package substitution_enron_fong;
import com.aliasi.chunk.Chunk;
import com.aliasi.chunk.Chunking;
import com.aliasi.sentences.MedlineSentenceModel;
import com.aliasi.sentences.SentenceChunker;
import com.aliasi.sentences.SentenceModel;
import com.aliasi.tokenizer.IndoEuropeanTokenizerFactory;
import com.aliasi.tokenizer.TokenizerFactory;
import com.aliasi.tokenizer.Tokenizer;
import com.aliasi.util.Files;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.Vector;

/** Use SentenceModel to find sentence boundaries in text */
public class SentenceBoundaryDemo {

    static final TokenizerFactory TOKENIZER_FACTORY = IndoEuropeanTokenizerFactory.INSTANCE;
    static final SentenceModel SENTENCE_MODEL  = new MedlineSentenceModel();
    static final SentenceChunker SENTENCE_CHUNKER = new SentenceChunker(TOKENIZER_FACTORY,SENTENCE_MODEL);
    
    public List<String> sen_boundary(String text) throws IOException {
    	List<String> tokenList = new ArrayList<String>();
    	List<String> whiteList = new ArrayList<String>();
    	Tokenizer tokenizer = TOKENIZER_FACTORY.tokenizer(text.toCharArray(),0,text.length());
    	tokenizer.tokenize(tokenList,whiteList);
    	String[] tokens = new String[tokenList.size()];
    	String[] whites = new String[whiteList.size()];
    	tokenList.toArray(tokens);
    	whiteList.toArray(whites);
    	int[] sentenceBoundaries = SENTENCE_MODEL.boundaryIndices(tokens,whites);
    	int sentStartTok = 0;
    	int sentEndTok = 0;
    	for (int i = 0; i < sentenceBoundaries.length; ++i) {
    	    sentEndTok = sentenceBoundaries[i];
    	    //System.out.println("SENTENCE "+(i+1)+": ");
    	    for (int j=sentStartTok; j<=sentEndTok; j++) {
    		//System.out.print(tokens[j]+whites[j+1]);
    	    }
    	   // System.out.println();
    	    sentStartTok = sentEndTok+1;
    	}
    	 return tokenList;
    }
    
    public Vector<String> Sentence_Chunker(String text){
    	Chunking chunking = SENTENCE_CHUNKER.chunk(text.toCharArray(),0,text.length());
    	Set sentences = chunking.chunkSet();
    	Vector<String> sentence_list = new Vector<String>();
    	String slice = chunking.charSequence().toString();
    	
    	for (Iterator it = sentences.iterator(); 
    			it.hasNext(); ) {
    		Chunk sentence = (Chunk)it.next();
    	    int start = sentence.start();
    	    int end = sentence.end();
    	    //System.out.println(slice.substring(start,end));
    	    sentence_list.add(slice.substring(start,end));
    	    }
    	return sentence_list;
    	}

	//System.out.println(tokenList.size() + " TOKENS");
	//System.out.println(whiteList.size() + " WHITESPACES");
//System.out.println(sentenceBoundaries.length 
			//   + " SENTENCE END TOKEN OFFSETS");
}

