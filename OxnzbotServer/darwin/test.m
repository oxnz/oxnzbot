#import <Foundation/Foundation.h>

int getResponse() {
	NSError *err;
	// URL to which data is posted
	NSURL *url = [NSURL URLWithString: @"http://oxnzbot.appspot.com/_ah/xmpp/"];
	// Key value to post
	NSString *postData = @"key1=value1&key2=value2";
	NSString *postLength = [NSString stringWithFormat: @"%d",
			 [postData length]];	// length of the data posted

	// send the request
	NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
	[request setURL: url];
	[request setCachePolicy: NSURLRequestReloadIgnoringCacheData];
	[request setTimeoutInterval: 20];
	[request setHTTPShouldHandleCookies: FALSE];
	[request setHTTPMethod: @"POST"];	// request method is POST

	[request addValue: @"text/plain; charset=utf-8"
		forHTTPHeaderField: @"Content-Type"];
	[request setValue: @"application/x-www-form-urlencoded"
		forHTTPHeaderField: @"Content-Type"];
	[request setValue: postLength forHTTPHeaderField: @"Content-Length"];
	//[request setHTTPBody: [postData dataUsingEncoding: NSASCIIStringEncoding
	//	AllowLossyConversion: YES]];

	// get the response
	NSData *responseData = [NSURLConnection sendSynchronousRequest: request
												 returningResponse: NULL
															 error: &err];
	if (!responseData) {
		NSLog(@"Connectoin Error: %@", [err localizedDescription]);
		return -1;
	}

	// Convrt the response data to string format
	// This is just for ease of use; you can choose to do something
	// else with the data
	NSLog(@"recieved %ld bytes", [responseData length]);
	NSString *responseString = [[NSString alloc] initWithData: responseData];
	NSLog(@"response: %@", responseString);
	return 0;
}

int main(int argc, char* argv[]) {
	getResponse();
	return 0;
}
