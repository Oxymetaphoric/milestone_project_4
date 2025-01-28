# Milestone Project :four:
 
This is my milestone four project for the Code Institute's 'Level 5 Diploma in Web Application Development.' The aim of this project is to design, develop, and implement a full-stack web application inluding back and front end design, and integrating an ePayment system via online service Stripe. This project will be a comprehensive library management web application using the python framework Django. This webapp will allow librarians and library staff to create, edit, and manage catalog records, check in and return items, and manage user accounts and stock control, providing an efficient, accessible tool for library inventory and user management. The application is aimed at libraries seeking a modern, flexible system to streamline their cataloging, inventory management, and user records, while also offering a user-friendly experience for library staff. This project will focus on the library staff and librarians use of the app, however possible future development could extend this project further to encompass a library customer system whereby users could login remotely, access their account information and interact with the library system.  

[LIVE SITE](https://library-management-lms-c0ccc240f065.herokuapp.com/)

---

## :world_map: Strategy

---

### Project Goals

#### User Goals:

- Access and search a library catalogue efficiently.
- Reserve, check out, and return items with ease. Access account information, including due dates and item availability. 
- View account history and any current items checked out.

#### Site Operator Goals:
        
- Maintain an organized and accessible record of the library's items.
- Track the availability and status of items to ensure proper circulation.
- Add, edit, and remove catalogue and user data to keep the library’s database accurate.
- Efficiently manage user accounts and item inventory.

#### Developer Goals:
        
- Create an intuitive and user-friendly application for both users and library staff.
- Ensure that the project is scalable and easy to maintain, with clear, well-documented code.
- Implement a reliable check-in/check-out system for managing item circulation.
- Ensure compatibility across devices with a responsive design.


---

## :earth_africa: Scope

---

### User Experience

#### Front End

The user interface will leverage bootstrap5 to offer a stream-lined, visually appealing experience. To maintain consistency across pages, the project uses Django’s template inheritance, creating a base template with core elements (such as navigation). This approach enables each page to extend the base, ensuring a uniform layout and reducing code duplication, making for a cleaner, more maintainable front-end design.

#### Back End

The database for this project uses SQLite, providing a lightweight and easily deployable solution for managing library catalog entries, inventory, and user records. Django's ORM allows for seamless database interactions, enabling complex queries, and maintaining data integrity across multiple related entities, such as catalog entries, inventory items, and user information. This setup ensures that catalog data and user records are efficiently managed and updated as required.

### Target Audience

- Library Staff and Managers: Seeking efficient ways to manage library inventory and keep track of catalog details.
- Library Members: Who will primarily interact with the search functionalities, browse catalog listings, and view availability.
- Community Libraries: Looking to modernize and streamline catalog management.
- Small Educational Institutions: Interested in organizing and managing a lending library for students and faculty.

### User Requirements and Expectations

- Easy, intuitive navigation
- Secure handling of user and item data
- Accessible interface for all types of users
- Ability to browse the catalog and check item availability
- Ability for staff to add, edit, and check in/out catalog items

### User Stories

#### First Time User

- As a first-time user, I want a clear homepage with an overview of catalog items and availability.
- As a first-time user, I want to search and browse the catalog based on title, author, or availability.
- As a first-time user, I want an intuitive experience while viewing catalog or account details.

- Returning User

- As a returning user, I want quick access to search and view catalog items.
- As a returning user, I want to view and update details related to library items, like availability and check-out dates.
- As a returning user, I want to log in securely to manage library inventory and users.

- Site Owner

- As a site owner, I want to manage and view inventory status with ease.
- As a site owner, I want to allow library members to browse and check the availability of items.
- As a site owner, I want to ensure data security for both catalog and user records.

Identified Tasks/Needs the Website Should Fulfill
Task/Need	Importance (1 -5)
Clear and accessible navigation	5
Responsiveness across devices	5
Browse and search library catalog	5
Manage user accounts securely	5
Add, edit, and update catalog and stock records	4
Update availability for catalog items	4
Generate reports or summaries on inventory status	3
Secure user login and account management	5
Direct 404 links to home if catalog or user not found	4
Accessibility

In building the library app, several accessibility features to keep in mind:

- Use of semantic HTML5 elements for improved structure.
- Descriptive link text to aid navigation.
- ARIA labels for interactive elements to ensure screen reader compatibility.
- Appropriate color contrast for readability.
- Legible, accessible fonts for ease of reading.
- Alternative text for any non-decorative images.
- Clearly labeled, accessible forms to improve user interaction.
---

## :bricks: Structure

---

### Database Structure

The library management system relies on a well-structured relational database to manage data on catalog items, stock inventory, and library users. Four main tables form the foundation of this database: CatalogueItem, StockItem, LibraryUser, and BorrowRecord. This schema ensures efficient querying, inventory tracking, and logging of user transactions, from borrowing to returning books.
Entity Relationship Diagram

An Entity Relationship Diagram (ERD) outlines the connections between these tables. Key relationships include:

- Each CatalogueItem entry can relate to multiple StockItem records.
- Each LibraryUser may have multiple BorrowRecord entries, tracking the user’s check-out history.
- StockItem connects both CatalogueItem and BorrowRecord, facilitating the check-out/check-in process and providing current availability.

### Schema Diagram

- A database schema diagram illustrates the field constraints, data types, and keys used in each table.


### Database Models

    CatalogueItem Table
    Stores details on individual book titles, including the primary BibNum, title, and other descriptive fields.
    Column Name	Data Type	Constraints	Key	Nullable
    bib_num	INT	AUTO_INCREMENT	PK	No
    title	STRING			No
    author	STRING			Yes
    genre	STRING			Yes
    publish_date	DATE			Yes

    StockItem Table
    Manages individual copies of cataloged books. Each StockItem references a CatalogueItem and includes status fields to track availability.
    Column Name	Data Type	Constraints	Key	Nullable
    stock_id	INT	AUTO_INCREMENT	PK	No
    bib_num	INT	FK (CatalogueItem)		No
    status	STRING	ENUM ('available', 'checked out')		No

    LibraryUser Table
    Records user information, from ID and username to library registration details.
    Column Name	Data Type	Constraints	Key	Nullable
    user_id	STRING	UNIQUE	PK	No
    username	STRING(50)			No
    email	STRING(255)			No
    is_admin	BOOL			No
    date_joined	DATETIME	DEFAULT CURRENT_TIMESTAMP		No

    BorrowRecord Table
    Links LibraryUser and StockItem, tracking each book borrowing transaction’s start and end dates.
    Column Name	Data Type	Constraints	Key	Nullable
    record_id	INT	AUTO_INCREMENT	PK	No
    user_id	STRING	FK (LibraryUser)		No
    stock_id	INT	FK (StockItem)		No
    borrow_date	DATETIME	DEFAULT CURRENT_TIMESTAMP		No
    return_date	DATETIME			Yes

### Site Features

Key features supported by this structure include:

- Account Management: Secure registration, login, and profile updates for library users.
- Search Functionality: Users can search the catalog to view or check out available books.
- Inventory Management: StockItem records help track physical availability of each catalog item.
- Borrowing and Returning: Each BorrowRecord entry logs check-outs and returns, helping manage due dates and availability.
- Admin Controls: Admin users can update catalog entries, manage stock items, and view borrowing history across users.

---

## :skull_and_crossbones: Skeleton

---

### Wireframes

#### Desktop Wireframes

#### Mobile Wireframes

---

## :art: Surface

---

### Design

#### Typography

#### Colour Palettes

### Technologies and Tools used

#### Languages

- **CSS3**
- **HTML5**
- **javaScript**
- **jQuery**
- **Markdown**
- **Regex**

#### Tools

- **[Tilix](https://gnunn1.github.io/tilix-web/)**
- **[Google Chrome](https://www.chrome.com/)**
- **[Firefox](https://www.firefox.com)**
- **[git](https://git-scm.com/)**
- **[VSCode for linux](https://code.visualstudio.com/)**
- **[Bootstrap 5.3.2](https://getbootstrap.com/)**
- **[jQuery](https://jquery.com/)**
- **[GitHub](https://www.github.com)**
- **[Pencil](https://pencil.evolus.vn/)**
- **[Coolors](https://coolors.co/)**
- **[Google Fonts](https://fonts.google.com/)**
- **[Photopea](https://www.photopea.com/)**
- **[hextorgba](https://rgbacolorpicker.com/hex-to-rgba)**
- **[amiresponsive](https://ui.dev/amiresponsive)**

---

## :microscope: Testing

---

### Testing Procedure
### Functional testing

| test                                           | verified |
| ---------------------------------------------- | -------- |
| | |

### User Stories Testing

#### - First Time User Testing


#### - Returning User Testing

#### - Site Owner Testing

### Desktop

### HTML/CSS Validators

### WAVE

### Lighthouse

---

### Mobile Testing

### Bug fixes


------------
---------------
-------------
--------------
---------------------
-----------------------------
--------------------------------
-----------------------------


## :loudspeaker: Deployment

---
 
---

## :heart: Credits and Acknowledgments

---

https://img.logoipsum.com/332.svg
My wonderful family!

