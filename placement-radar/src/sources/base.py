from abc import ABC, abstractmethod

class BaseSource(ABC):
    @property
    @abstractmethod
    def source_name(self):
        """Return the name of the source (e.g., 'GitHub', 'Reddit')"""
        pass

    @abstractmethod
    def fetch(self):
        """
        Fetch opportunities.
        Must return a list of dictionaries in the format:
        {
            "title": str,
            "link": str,
            "source": self.source_name
        }
        """
        pass
