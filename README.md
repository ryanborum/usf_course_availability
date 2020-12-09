# usf_course_availability

**Usage:**
```
py course_checker.py <school_term> <CRN or Course Subj/Num>
```
**Example**
```
py course_checker.py Fall2020 ENC1101
```


**Author - Ryan Borum**  
Uses the BeautifulSoup python library to scrape a course search web form looking for seat openings and returning the CRN numbers via Pushbullet alert.
*Note*: This will no longer be functional as the course management system has transferred to a different platform.

**Depends On:**
Python 3.7.2  
BeautifulSoup4  
Pushbullet API (optional)
