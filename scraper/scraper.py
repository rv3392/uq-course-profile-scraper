import urllib.request

import bs4

import course_profile

class CourseProfileURLException(Exception):
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

        try:
            self.course_profile_url = self._get_course_profile_url()
        except CourseProfileURLException:
            print("Profile Not Available!")
            return

        print(self.course_profile_url)

    def scrape(self):
        """ Scrape the course profile of the requested course offering."""
        pass

    def _get_course_profile_url(self) -> str:
        """Gets the course profile URL using the course offerings page.
        
        Returns:
            str: the URL to the course profile's first section
            
        Raises:
            CourseProfileURLException: if no URL is found for the
                parameters provided in the class initialisation
        """

        # Load page from UQ website
        course_offering_request = urllib.request.Request(self._course_url, 
                headers={'User-Agent':'Course Profile API'})
        page_html = urllib.request.urlopen(course_offering_request).read()
        page = bs4.BeautifulSoup(page_html, features="html.parser")

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
                    raise CourseProfileURLException()

        raise CourseProfileURLException()

class InteractiveCourseProfileScraper(CourseProfileScraper):
    """ Used to interactively run the scraper from the terminal. """
    def __init__(self):
        super.__init__(self)
        pass

def main():
    CourseProfileScraper("CSSE2310", "Semester 1, 2020")

if __name__ == "__main__":
    main()