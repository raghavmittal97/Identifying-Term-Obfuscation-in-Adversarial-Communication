package substitution_enron_fong;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import com.aliasi.hmm.HiddenMarkovModel;
import com.aliasi.hmm.HmmDecoder;
import com.aliasi.tag.Tagging;
import com.aliasi.tokenizer.RegExTokenizerFactory;
import com.aliasi.tokenizer.Tokenizer;
import com.aliasi.tokenizer.TokenizerFactory;
import com.aliasi.util.Streams;

public class RunMedPost {

	static TokenizerFactory TOKENIZER_FACTORY = new RegExTokenizerFactory(
			"(-|'|\\d|\\p{L})+|\\S");

	public static void getWords(String line, List<String> tokenList) throws ClassNotFoundException,
			IOException {
		String filename = "./pos-en-general-brown.HiddenMarkovModel";
		//System.out.println("Reading model from file=" + filename);
		FileInputStream fileIn = new FileInputStream(filename);
		ObjectInputStream objIn = new ObjectInputStream(fileIn);
		HiddenMarkovModel hmm = (HiddenMarkovModel) objIn.readObject();
		Streams.closeQuietly(objIn);
		HmmDecoder decoder = new HmmDecoder(hmm);

		char[] cs = line.toCharArray();
		Tokenizer tokenizer = TOKENIZER_FACTORY.tokenizer(cs, 0, cs.length);
		String[] tokens = tokenizer.tokenize();
		tokenList = Arrays.asList(tokens);

		firstBest(tokenList, decoder);
		//System.out.println("output of firstbest: " + fb);
		//return filteredFirstBest(tokenList, decoder);
	}

	static List<String> firstBest(List<String> tokenList, HmmDecoder decoder) {
		List<String> words_with_tags = new ArrayList<String>();
		Tagging<String> tagging = decoder.tag(tokenList);
		for (int i = 0; i < tagging.size(); ++i)
			words_with_tags.add(tagging.tag(i));
		return words_with_tags;
	}

	static HashMap<String, String> filteredFirstBest(List<String> tokenList, HmmDecoder decoder) {
		String[] tags = { "ql", "qlp", "jj", "jj$", "jj+jj", "jjr", "jjr+cs",
				"jjs", "jjt", "rb", "rb$", "rb+bez", "rb+cs", "rbr", "rbr+cs",
				"rbt", "rn", "rp", "rp+in" };
		List<String> acceptable_tags = Arrays.asList(tags);
		HashMap<String, String> filtered_words = new HashMap<String, String>();
		Tagging<String> tagging = decoder.tag(tokenList);
		for (int i = 0; i < tagging.size(); ++i)
			if (acceptable_tags.contains(tagging.tag(i))) {
				filtered_words.put(tagging.token(i), tagging.tag(i));
			}
		
		return filtered_words;
	}
}
