package java_sync;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Projections;

import java.io.IOException;
import java.net.InetAddress;
import java.util.List;
import java.util.logging.Level;

import org.bson.Document;
import org.elasticsearch.action.bulk.BulkRequestBuilder;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentBuilder;

import static org.elasticsearch.common.xcontent.XContentFactory.*;

public class JavaSync {
	@SuppressWarnings("unchecked")
	public static void main(String[] args) throws IOException {
		
		long bulkBuilderLength = 0;
		Settings settings = Settings.settingsBuilder()
		        .put("cluster.name", "elasticsearch").build();
		TransportClient client = TransportClient.builder().settings(settings).build()
		        .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("localhost"), 9300));
		BulkRequestBuilder bulkRequest = client.prepareBulk();
		java.util.logging.Logger.getLogger("org.mongodb.driver").setLevel(Level.SEVERE);
		MongoClient mongoClient = new MongoClient( "localhost" , 27017 );
		MongoDatabase mongodb = mongoClient.getDatabase("elasticPlaces");
		MongoCollection<Document> collection = mongodb.getCollection("places");
		MongoCursor<Document> cursor = collection.find().projection(Projections.include("name", "_id", "types", "formatted_address", "rating", "geometry")).iterator();
		while (cursor.hasNext()) {
	        Document place = cursor.next();
		    String id = place.get("_id").toString();
		    String name = place.get("name").toString();
		    String formatted_address = place.get("formatted_address").toString();
		    String rating = place.get("rating").toString();
		    String lat = ((Document) ((Document) place.get("geometry")).get("location")).get("lat").toString();
		    String lon = ((Document) ((Document) place.get("geometry")).get("location")).get("lng").toString();
		    List<String> types = (List<String>) place.get("types");
		    XContentBuilder builder = jsonBuilder().startObject()
		    		.field("name", name)
		    		.field("formatted_address", formatted_address)
		    		.field("rating", rating)
		    		.startObject("location")
		    			.field("lat", lat)
		    			.field("lon", lon)
		    		.endObject()
		    		.startArray("types");
				    for (String type : types) {
				    	builder.value(type);
					}
				    builder.endArray();
		    builder.endObject();
		    bulkRequest.add(client.prepareIndex("elasticplaces", "places", id).setSource(builder));
			bulkBuilderLength++;
		    
			//batch size 1000
			if(bulkBuilderLength % 1000== 0){
			      BulkResponse bulkRes = bulkRequest.execute().actionGet();
			      if(bulkRes.hasFailures()){
			      }
			      bulkRequest = client.prepareBulk();
			}
		}
		if(bulkRequest.numberOfActions() > 0){
		   System.out.println("##### " + bulkBuilderLength + " data indexed.");
		   BulkResponse bulkRes = bulkRequest.execute().actionGet();
		   if(bulkRes.hasFailures()){
		      System.out.println("##### Bulk Request failure with error: " +   bulkRes.buildFailureMessage());
		   }
		   bulkRequest = client.prepareBulk();
		}
		client.close();
		mongoClient.close();
	}
}
