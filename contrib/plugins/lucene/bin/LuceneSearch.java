import java.net.URLDecoder;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.Searcher;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.Hits;
import org.apache.lucene.queryParser.QueryParser;

class LuceneSearch {
    public static void main(String[] args) {
        try {

	    Searcher searcher = new IndexSearcher(args[0]);
	    Analyzer analyzer = new StandardAnalyzer();

	    String line = URLDecoder.decode(args[1]);

	    Query query = QueryParser.parse(line, "contents", analyzer);

	    Hits hits = searcher.search(query);

	    for (int i = 0; i < hits.length(); i++) {
		System.out.println(hits.doc(i).get("url"));
	    }

	    searcher.close();

        } catch (Exception e) {
	    e.printStackTrace();
	    System.exit(9);
        }
    }
}
