from enum import Enum
from typing import List

import bs4

import course_profile
import utils.page_loader as page_loader

class CourseProfileURLException(Exception):
    pass

class InvalidScraperOptionException(Exception):
    pass

class CourseProfileScraper:
    """Reads the Course Profile of a course from the UQ website.

    Create an instance of CourseProfileScraper with the course_code,
    semester, location and mode of the desired course offering. Call
    scrape() on this instance to get the details from this 
    course_profile.
    
    Attributes:
        course_code (str): course code for the course to be scraped
        semester (str): semester for the offering should be of the
            form ("Semester <n>, <year>")
        location (str, optional): location for the offering
        mode (str, optional): delivery mode for the offering
    """

    BASE_URL = "https://my.uq.edu.au/programs-courses/course.html?course_code="

    def __init__(self, course_code: str, semester: str,
            location: str = "St Lucia", mode: str = "Internal"):
        """Constructor for CourseProfileScraper."""

        self._course_code = course_code
        self._semester = semester
        self._location = location
        self._mode = mode
        self._course_url = self.BASE_URL + self._course_code

        self.SCRAPER_OPTIONS = { 
                "all" : self._scrape_all, 
                "assessment" : self._scrape_assessments 
            }

        try:
            self.course_profile_url = self._get_course_profile_url()
        except CourseProfileURLException:
            raise

        print(self.course_profile_url)

    def scrape(self, selected_option : str) -> course_profile.CourseDetails:
        """Scrape the course profile of the requested course offering.
        
        Parameters:

        Returns:
        
        Raises:
        
        """

        if (selected_option not in self.SCRAPER_OPTIONS):
            raise InvalidScraperOptionException

        return self.SCRAPER_OPTIONS[selected_option]()
        
    def _scrape_all(self):
        return "This functionality is not implemented"

    def _scrape_assessments(self):
        """Scrape all assessments from the course profile.

        Each assessment dictionary includes details about the task name,
        due date, format, etc. The format is defined in course_profile.py

        Returns: 
            dict: A dictionary of the Assessment format for an assessment in
                a particular course profile
        """
        assessment_url = self.course_profile_url.replace("section_1", "section_5")
        page = page_loader.get_page_soup(assessment_url)

        assessments_html = page.find(name="div", attrs={"id":"assessmentDetail"})

        for br in assessments_html.find_all("br"):
            br.extract()

        assessments = []

        assessment_tags = {}
        current_tag = assessments_html.find("h4")
        while(current_tag != None):
            if (current_tag.name == "hr"):
                assessments.append(assessment_tags)
                assessment_tags = {}

            # All details are of the form "<strong>DETAIL_NAME:</strong> DETAIL"
            if (current_tag.name == "strong"):
                detail_name_tag = current_tag.text.strip().replace(" ", "_") \
                        .replace(":", "").lower()  
                current_tag, assessment_tags[detail_name_tag] = \
                        self._parse_assessment_detail(current_tag)

            current_tag = current_tag.next_sibling

        return assessments

    def _parse_assessment_detail(self, detail_name_tag):                            
        current_tag = detail_name_tag
        if (current_tag.next_sibling == "\n"):
            current_tag = current_tag.next_sibling
        
        detail_tag = ""
        if (type(current_tag.next_sibling) != bs4.NavigableString):
            detail_tag = current_tag.next_sibling.text
        else:
            detail_tag = current_tag.next_sibling
        detail_tag = detail_tag.strip().replace("\n", "")
        
        return current_tag, detail_tag

    def get_scraper_options(self) -> List[str]:
        """Gets a list of the options for the scraper. """
        return list(self.SCRAPER_OPTIONS.keys())

    def _get_course_profile_url(self) -> str:
        """Gets the course profile URL using the course offerings page.
        
        Returns:
            str: the URL to the course profile's first section
            
        Raises:
            CourseProfileURLException: if no URL is found for the
                parameters provided in the class initialisation
        """

        # Load page from UQ website
        page = page_loader.get_page_soup(self._course_url)

        # Search for the provided semester, location and mode using rows of
        # the offerings tables
        all_offering_rows = page.find_all('tr')
        for row in all_offering_rows:
            cells = row.find_all('td')
            offering_semester = cells[0].get_text().strip("\n")
            offering_location = cells[1].get_text().strip("\n")
            offering_mode = cells[2].get_text().strip("\n")
            if (offering_semester == self._semester 
                    and offering_location == self._location
                    and offering_mode == self._mode):
                try:
                    # Cell [3] contains a-link with href to Course Profile
                    return cells[3].find('a')['href']
                except:
                    raise CourseProfileURLException("Profile not available!")

        raise CourseProfileURLException("Profile not available!")

class InteractiveCourseProfileScraper(CourseProfileScraper):
    """ Used to interactively run the scraper from the terminal. """
    def __init__(self):
        super.__init__(self)
        pass

def main():
    try:
        scraper = CourseProfileScraper("CSSE2310", "Semester 1, 2020")
        print(scraper.scrape(selected_option="assessment"))
    except:
        print("Scraper initialisation failed: ") #TODO: Add the exact reason
        return

if __name__ == "__main__":
    main()