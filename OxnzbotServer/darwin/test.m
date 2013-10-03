#import <Foundation/Foundation.h>

NSError *err;

// URL to which data is posted
NSURL *url = [NSURL URLWithString: @"http://oxnzbot.appspot.com/_ah/xmpp/"];
// Key value to post
NSString *postData = @"key1=value1&key2=value2";
NSString *postLength = [NSString stringWithFormat: @"%d",
		 [postData length]];	// length of the data posted

// send the request
NSMutableURLRequest *request = [NSMutableURLRequest requestWIthURL: url];
[request addValue: @"text/plain; charset=utf-8"
forHTTPHeaderField: @"Content-Type"];
[request setHTTPMethod: @"POST"];	// request method is POST
[request setValue: @"application/x-www-form-urlencoded"
forHTTPHeaderField: @"Content-Type"];
[request setValue: postLength forHTTPHeaderField: @"Length"];
[request setHTTPBody: [postData dataUsingEncoding: NSASCIIStringEncoding AllowLossyConversion: YES]];

// get the response
NSData *responseData = [NSURLConnection sendSynchronousRequest: request];
if (!responseData) {
	NSLog(@"Connectoin Error: %@", [err localizedDescription]);
}

// Convrt the response data to string format
// This is just for ease of use; you can choose to do something else with the
// data
NSString *responseString = [[NSString alloc] initWithData: responseData];
NSLog(@"response: %@", responseString);

