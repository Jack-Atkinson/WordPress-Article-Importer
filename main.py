import csv
import os
from os import path

article_csv = "C:\\Users\\jatkinson\\Desktop\\articles.csv";
articles_dir = "C:\\Users\\jatkinson\\Desktop\\articles"

fieldnames = ("post_name", "post_title", "post_status", "post_content", "post_excerpt", "post_author", "post_parent", "post_date", "post_image", "comment_status", "ping_status")

class FindString:
	def __init__(self, pattern, content, delimiter, offset=0):
		self.pattern = pattern;
		self.content = content;
		self.delimiter = delimiter;
		self.offset = offset;

	def results(self, start_index=-1, previous=""):
		pos = self.content.find(self.pattern, start_index + 1);
		if pos == -1:
			return [];
		else:
			pos += self.offset;
		link = self.content[pos:].partition(self.delimiter)[0];
		return [link] + self.results(pos, link)

class Excel:
	def __init__(self, filename, method):
		self.file = open(filename, method);
		if method == 'w':
			self.pipe = csv.DictWriter(self.file, fieldnames=fieldnames);
			headers = dict((n, n) for n in fieldnames);
			self.pipe.writerow(headers);
		elif method == 'r':
			self.pipe = csvDictReader(self.file);
		else:
			print("Unknown method for pipe.");

	def __enter__(self):
		return self;

	def writerow(self, content):
		self.pipe.writerow(content);

	def cleanup(self):
		self.file.close();

if __name__ == "__main__":
	article_csv = Excel(article_csv, 'w');
	articles = [f for f in os.listdir(articles_dir)
	                  if path.isfile(os.path.join(articles_dir, f))];
	for article in articles:
		content = file(os.path.join(articles_dir, article), 'r').read()
		title = FindString("<h1 class=\"title\">", content, "</h1>", 18)
		date = FindString("<span class=\"submitted\">Posted ", content, "</span", 31)
		if title.results() == [] or date.results() == []:
			continue;

		date = date.results()[0].split(' ');
		months = {"January" : "Jan",
		          "February" : "Feb",
		          "March" : "Mar",
		          "April" : "Apr",
		          "May" : "May",
		          "June" : "Jun",
		          "July" : "Jul",
		          "August" : "Aug",
		          "September": "Sep",
		          "October" : "Oct",
		          "November" : "Nov",
		          "December" : "Dec"};
		date[0] = months[date[0]]
		date.pop(3)
		print date
		content = content.replace("<h1 class=\"title\">" + title.results()[0] + "</h1>", "");
		title = title.results()[0].replace("\xe2\x80\x94", "");
		csv_version = {"post_name" : article[:-5],
		               "post_title" : title,
		               "post_status" : "publish",
		               "post_content" : content,
		               "post_excerpt" : "",
		               "post_author" : "HolidayLED",
		               "post_parent" : "0",
		               "post_date" : ' '.join(date),
		               "post_image" : "",
		               "comment_status" : "open",
		               "ping_status" : "open"};
		article_csv.writerow(csv_version);
	article_csv.cleanup();
