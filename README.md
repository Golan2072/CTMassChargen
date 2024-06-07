# CTMassChargen
Classic Traveller RPG mass character generator

This data-driven program will mass-generate Classic Traveller RPG characters for ease of use as PCs or NPCs in your game. The final version will output the characters to either an Excel file or a PDF file.

By Omer Golan-Joel, golan2072@gmail.com

Version 0.3.1 - June 7th, 2024
- Fixed a bug where rank can exceed 6, causing a crash.
- Improved Excel layout.
- Now number-only columns in the Excel output are outputted in Integers, not Strings.

Version 0.2 - June 7th, 2024
- Now generates characters to excel, asks the user for career and number of characters.
- Appends to existing Excel file, if it exsists, otherwise creates a new file.
- Now weapons in inventory at least partially match weapon skills.

Version 0.1.2 - June 7th, 2024
- Initial commit. Can generate a single random character to the command line.
- Includes name databases.
- Includes a JSON file with the 6 classical careers.
