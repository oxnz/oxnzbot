<?php
/*
     Filename: OxnzRobotServer.php
  Description: 

      Version: 0.1
      Created: 2013-10-11 15:01:51
  Last-update: 2013-10-11 15:29:10
     Revision: None

       Author: Oxnz
        Email: yunxinyi@gmail.com

Revision history:
	Date Author Remarks
*/

//CONFIG:
define('DB_NAME', 'database_name_here');
define('DB_USER', 'username_here');
define('DB_PASSWORD', 'password_here');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8');

class DBHelper {
}

class CommandServer {
}

class ControlServer {
}

class OxnzbotServer {
	private function handleGet() {
		//echo "get<br>";
		//var_dump($_GET);
		echo "sleep 10";
	}
	private function handlePost() {
		echo "post";
		var_dump($_POST);
	}
	private function handleRequest() {
		//var_dump($_SERVER);
		//var_dump($_REQUEST);
		if ($_SERVER["REQUEST_METHOD"] == "POST") {
			$this->handlePost();
		} elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
			$this->handleGet();
		}
	}
	public function run() {
		$this->handleRequest();
	}
}

function main() {
	try {
		$server = new OxnzbotServer;
		$server->run();
	} catch (Exception $e) {
		echo 'Exception: ', $e->getMessage(), '\n';
	}
}


main();

?>

<form method="post"
	action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>"> 
	from: <input type="text" name="from" /><br />
	command: <input type="text" name="command" /><br />
	status: <input type="number" name="status" /><br />
	output: <input type="text" name="output" /><br />
	<input type="submit" value="Submit" />
</form>
