package substitution_enron_fong;
import java.util.ArrayList;

import com.cybozu.labs.langdetect.Detector;
import com.cybozu.labs.langdetect.DetectorFactory;
import com.cybozu.labs.langdetect.LangDetectException;
import com.cybozu.labs.langdetect.Language;

public class Detect_Language {
	//static String profileDirectory = "/Users/agrawal/Documents/HnEVDO/Twitter_YT/langdetect-03-03-2014/profiles";
	private static void languagedetection(String text) {
		try {
			//init(text);
			String lang=detect(text);
			System.out.println(lang);
			detectLangs(text);
			
		} catch (LangDetectException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	public void init(String profileDirectory)throws LangDetectException {
        DetectorFactory.loadProfile(profileDirectory);
        
    }
    public static String detect(String text_1){
        Detector detector;
        String value=null;
		try {
			detector = DetectorFactory.create();
		
        detector.append(text_1);
        value=detector.detect();
		} catch (LangDetectException e) {
			value="-";
			System.out.println(e);
		}
		return value;
    }
    public static ArrayList<Language> detectLangs(String text) throws LangDetectException {
        Detector detector = DetectorFactory.create();
        detector.append(text);
        return detector.getProbabilities();
    }

}
