package io.github.oxnz.OxnzBotServer;

import java.net.HttpURLConnection;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.util.List;
import java.util.ArrayList;
import java.util.Observable;
import java.util.Observer;
import java.util.Date;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class OxnzBotServer implements Observer {
	static class Helper {
		public static String ts() {
			String timestamp = String.format(
					"%1$tY/%1$tM/%1$td %1$tH:%1$tm:%1$tS", new Date());
			return timestamp;
		}
	};
	class Command {
		public Command(String cmd) {
			command = cmd;
		}
		public void setCommand(String cmd) {
			command = cmd;
		}
		public String getCommand() {
			return command;
		}
		public void setExecuted(boolean executed_) {
			executed = executed_;
		}
		public boolean getExecuted() {
			return executed;
		}
		public void setResult(String result_) {
			result = result_;
		}
		public String getResult() {
			return result;
		}
		public void setRetCode(int code) {
			retcode = code;
		}
		public int getRetCode() {
			return retcode;
		}
		public String toString() {
			return "Command: " + command + (executed ? (
						" [executed]\nreturn code: " + retcode + "\nresult:"
						+ (result.length() == 0 ? ": None" : result)
						) : " [not executed yet]");
		}
		private String command;
		private boolean executed = false;
		private String result;
		private int retcode;
	};
	class CmdPullServer extends Observable implements Runnable {
		private List<Command> resultPool = new ArrayList<Command>();
		private HttpsURLConnection conn;
		private String url;
		public void setURL(String url_) {
			url = url_;
			url += "oxnz";
		}
		private Command pull() {
			try {
				System.out.println("pulling ...");
				Command cmd = new Command("ls -l");
				return cmd;
			} catch (Exception e) {
				e.printStackTrace();
				return pull();
			}
		}
		public void run() {
			while (true) {
				System.out.println(Helper.ts() + ": puller run...");
				try {
					Thread.sleep(1000);
					Command cmd = pull();
					setChanged();
					notifyObservers(cmd);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
	};
	class RetPushServer implements Runnable, Observer {
		private List<Command> cmdPool = new ArrayList<Command>();
		private HttpsURLConnection conn;
		private String url;
		public void update(Observable ob, Object obj) {
			System.out.println(Helper.ts() + ": pusher recieved notify:\n"
					+ obj);
			cmdPool.add((Command)obj);
		}
		public void setURL(String url_) {
			url = url_;
		}
		private void push(Command cmd) {
			try {
				System.out.println("pushing....");
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		public void run() {
			while (true) {
				System.out.println(Helper.ts() + ": pusher run...");
				try {
					Thread.sleep(1000);
					if (cmdPool.size() > 0) {
						Command cmd = cmdPool.get(0);
						push(cmd);
						cmdPool.remove(0);
					} else {
						Thread.sleep(1);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
	};
	class ExecuteServer extends Observable implements Runnable, Observer {
		private List<Command> cmdPool = new ArrayList<Command>();
		public void update(Observable ob, Object obj) {
			System.out.println(Helper.ts() + ": exetor recieved notify:\n"
					+ obj);
			cmdPool.add((Command)obj);
		}
		public void run() {
			while (true) {
				try {
					System.out.println(Helper.ts() + ": exetor run...");
					if (cmdPool.size() > 0) {
						Command cmd = cmdPool.get(0);
						execute(cmd);
						cmdPool.remove(0);
					} else {
						Thread.sleep(1000);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
		private Runtime runtime = Runtime.getRuntime();
		private StringBuilder stringBuilder = new StringBuilder();
		private void execute(Command cmd) {
			try {
				System.out.println("executing: " + cmd.getCommand());
				Process proc = runtime.exec(cmd.getCommand());
				BufferedReader stdout = new BufferedReader(new
						InputStreamReader(proc.getInputStream()));
				BufferedReader stderr = new BufferedReader(new
						InputStreamReader(proc.getErrorStream()));
				stringBuilder.setLength(0);
				String tmp = "";
				while ((tmp = stdout.readLine()) != null) {
					stringBuilder.append(tmp);
					stringBuilder.append('\n');
				}
				if (stringBuilder.length() > 0) {
					stringBuilder.insert(0, "\n[stdout]:\n");
				}
				int len = stringBuilder.length();
				while ((tmp = stderr.readLine()) != null) {
					stringBuilder.append(tmp);
					stringBuilder.append('\n');
				}
				if (stringBuilder.length() > len) {
					stringBuilder.insert(len, "\n[stderr]:\n");
				}
				cmd.setRetCode(proc.waitFor());
				cmd.setExecuted(true);
				cmd.setResult(stringBuilder.toString());
				System.out.println("result: " + cmd.getResult()
						+ "\nreturn code: " + cmd.getRetCode());
				setChanged();
				notifyObservers(cmd);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	};
	public void update(Observable ob, Object obj) {
		System.out.println("Should not happend");
	}
	public int loop() {
		CmdPullServer pullServer = new CmdPullServer();
		RetPushServer pushServer = new RetPushServer();
		ExecuteServer execServer = new ExecuteServer();
		pullServer.setURL(
				"https://oxnzbot.appspot.com/_ah/xmpp/__0x01379/?from=");
		pushServer.setURL("https://oxnzbot.appspot.com/_ah/xmpp/__0x01379");
		pullServer.addObserver(execServer);
		execServer.addObserver(pushServer);
		Thread pullThread = new Thread(pullServer);
		Thread pushThread = new Thread(pushServer);
		Thread execThread = new Thread(execServer);
		pushThread.start();
		execThread.start();
		pullThread.start();

		return 0;
	}
	public boolean test() {
		Command cmd = new Command("ls /");
		System.out.println(cmd);
		cmd.setExecuted(true);
		cmd.setResult("drwxrwxrwx ls.txt 2012 00 12 12:12:12 1.2 kb\ndrwx");
		cmd.setRetCode(1);
		System.out.println(cmd);
		return true;
	}
	public static void main(String[] args) {
		try {
			OxnzBotServer server = new OxnzBotServer();
			server.loop();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
};
