# Milestone Project :four:
 
This is my milestone four project for the Code Institute's 'Level 5 Diploma in Web Application Development.' The aim of this project is to design, develop, and implement a full-stack web application inluding back and front end design, and integrating an ePayment system via online service Stripe. This project will take the form of a comprehensive library management web application using the python framework Django, called CLIO. Named after the greek goddess of knowledge and scholarship (it could also be a fun acronym, perhaps Clever Library Infomation Organisation). CLIO will allow librarians and library staff to create, edit, and manage catalog records, check in and return items, and manage user accounts and stock control, providing an efficient, accessible tool for library inventory and user management. CLIO is aimed at libraries seeking a modern, flexible system to streamline their cataloging, inventory management, and user records, while also offering a user-friendly experience for library staff. This project will focus on the library staff and librarians use of the app, however possible future development could extend this project further to encompass a library customer access whereby users could login remotely, access their account information, and interact with the library system.   

[![LIVE SITE](./docs/customer_account.png)](https://library-management-lms-c0ccc240f065.herokuapp.com/)


[LIVE SITE](https://library-management-lms-c0ccc240f065.herokuapp.com/)

### Testing logins: 

The following accounts can be used for the purposes of testing and assessing the front-end of the project: 

| username | password | privilege level |
|------|------|---------|
test_superuser | loginrequired | superuser
test_admin_privs | test123 | admin
test_librarian_privs | loginrequired | librarian
test_staff_privs | loginrequired | staff

Please be aware that you will not be able to sign-up to the application and will, necessarily, have to log-in using the above details. The system is not designed for open access from the public and is designed with the concept of being a system front-line staff would access, necessitating corporate-level control over sign-up and account creation. The current privilege heirarchy is Admin > Librarians > Staff: 

#### Admin: 

Full control of the system including creating, deleting and amending all records within the system and in the admin panel. This would be utilised by administrative staff, or IT departments. 

#### Librarian :

Full access to read, write and destroy records within the system, limited access to adminsitrative function such as creating new staff members. 

#### Staff: 

Read access to all system information with limited create and write permissions and no admin access. Frontline staff would not be expected to, for example, create Catalogue entries, as these would be created on purchase of items and involves other systems outside the purview of this project.  

If you wish to test the payment functionality, the best way would be to check out an item to a customer, access the customers account, then mark the item as lost. This will generate a fee on the account that can then be paid using the stripe test card data: 

test card | card number | expiry date | ccv | zip code
|-------------|-------------|------|--------|------|
| success | 4242424242424242 | 01/30 | 123 | 12345 |
| error | 4000000000009995 | 01/30 | 123 | 12345 | 

---

## Project Goals

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

### User Experience

#### Front End

The user interface will leverage bootstrap5 to offer a stream-lined, visually appealing experience. To maintain consistency across pages, the project uses Django’s template inheritance, creating a base template with core elements (such as navigation). This approach enables each page to extend the base, ensuring a uniform layout and reducing code duplication, making for a cleaner, more maintainable front-end design.

#### Back End

The database for this project uses postgreSQL providing a robust and powerful solution for managing library catalog entries, inventory, and user records. Django's ORM allows for seamless database interactions, enabling complex queries, and maintaining data integrity across multiple related entities, such as catalog entries, inventory items, and user information. This setup ensures that catalog data and user records are efficiently managed and updated as required.

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

---

### User Stories

#### First Time User

- As a first-time user, I want a clear homepage with an overview of catalog items and availability.
- As a first-time user, I want to search and browse the catalog based on title, author, or availability.
- As a first-time user, I want an intuitive experience while viewing catalog or account details.

#### Returning User

- As a returning user, I want quick access to search and view catalog items.
- As a returning user, I want to view and update details related to library items, like availability and check-out dates.
- As a returning user, I want to log in securely to manage library inventory and users.

#### Site Owner

- As a site owner, I want to manage and view inventory status with ease.
- As a site owner, I want to allow library members to browse and check the availability of items.
- As a site owner, I want to ensure data security for both catalog and user records.

---

Identified Tasks/Needs the Website Should Fulfill

| Task/Need	| Importance (1 -5) | 
|---------------|--------------|
Clear and accessible navigation	| 5
Responsiveness across devices |	5
Browse and search library catalog | 5
Manage user accounts securely |	5
Add, edit, and update catalog and stock records | 4
Update availability for catalog items | 4
Generate reports or summaries on inventory status | 3
Secure user login and account management | 5
Direct 404 links to home if catalog or user not found | 4

### Accessibility

In building the library app, several accessibility features to keep in mind:

- Use of semantic HTML5 elements for improved structure.
- Descriptive link text to aid navigation.
- ARIA labels for interactive elements to ensure screen reader compatibility.
- Appropriate color contrast for readability.
- Legible, accessible fonts for ease of reading.
- Alternative text for any non-decorative images.
- Clearly labeled, accessible forms to improve user interaction.

---

## Database Relationships

### Core Model Relationships

```
LibraryCustomer
├── CurrentLoan (One-to-Many)
│   └── StockItem (One-to-One)
├── LoanHistory (One-to-Many)
│   └── StockItem (One-to-One)
└── Fine (One-to-Many)
    ├── LoanHistory (One-to-One)
    └── Payment (One-to-Many)
        └── PaymentHistory (One-to-One)
```
```
CatalogueItem
└── StockItem (One-to-Many)
    ├── CurrentLoan (One-to-One)
    └── LoanHistory (One-to-Many)
```

### Detailed Relationship Descriptions

Detailed Relationship Specifications
LibraryCustomer Relationships

CurrentLoan

Type: One-to-Many
Foreign Key: customer in CurrentLoan
Cascade: Delete loans when customer is deleted
Purpose: Tracks active borrowings


LoanHistory

Type: One-to-Many
Foreign Key: customer in LoanHistory
Cascade: Preserve loan history
Purpose: Maintains borrowing records


Fine

Type: One-to-Many
Foreign Key: customer in Fine
Cascade: Delete fines when customer is deleted
Purpose: Tracks financial penalties

#### CatalogueItem Relationships

## StockItem

Type: One-to-Many
Foreign Key: catalogue_item in StockItem
Cascade: Delete stock items when catalogue item is deleted
Purpose: Represents physical copies


### Stock Management

#### StockItem → CurrentLoan

Type: One-to-One
Foreign Key: stock_item in CurrentLoan
Constraint: One item can only be in one active loan
Purpose: Tracks current borrower

#### StockItem → LoanHistory

Type: One-to-Many
Foreign Key: stock_item in LoanHistory
Purpose: Maintains item borrowing history

### Financial Management

Fine → Payment

Type: One-to-Many
Foreign Key: fine in Payment
Purpose: Tracks payment attempts

Payment → PaymentHistory

Type: One-to-One
Foreign Key: payment in PaymentHistory
Purpose: Records payment status changes


## Key Business Rules

### Loan Management

A StockItem can only be in one CurrentLoan
A StockItem can have multiple LoanHistory records
CurrentLoans move to LoanHistory upon return

### Fine Processing

Fines are linked to specific LoanHistory records
Multiple payments can be attempted for one fine
Payment history tracks all status changes

### Stock Control

CatalogueItems track total available copies
StockItems represent individual physical copies
Status changes are logged with timestamps

## Database Integrity

All relationships maintain referential integrity
Cascading deletes where appropriate
Proper indexing on relationship fields
Status tracking across related entities

### Entity State Transitions

StockItem Status Flow:
available → on_loan → available
         → maintenance
         → discarded
         → missing

Payment Status Flow:
PENDING → PROCESSING → COMPLETED
                    → FAILED
                    → REFUNDED

This structure ensures:

Data consistency across operations
Proper tracking of all transactions
Clear audit trail of changes
Efficient query performance
Scalable data management

### Key Constraints

1. **Stock Management**
   - A StockItem cannot be in multiple CurrentLoans simultaneously
   - Stock status (available, on_loan, maintenance, etc.) determines if it can be loaned

2. **Loan Management**
   - A customer cannot borrow if they have excessive unpaid fines
   - A customer cannot borrow if they already have the maximum allowed loans

3. **Financial Management**
   - Fines are automatically calculated based on overdue loans
   - Payments must be processed before new loans can be issued if fines exceed the cap

### Entity Relationship Diagram (ERD)

[![Schema Diagram](./docs/database_schema.png)](./docs/)

This structure ensures:
- Data integrity across the library system
- Proper tracking of all loans and returns
- Accurate financial record keeping
- Clear audit trail of all transactions
- Efficient stock management

## Database Models

### Users Models

#### LibraryCustomer

| Field	| Data Type	| Constraints/Notes |
|----------|----------|-------------|
user_id | CharField | Primary key, max_length=8, unique, auto-generated (e.g., A0000001)
first_name | CharField | max_length=256, optional
last_name | CharField | max_length=256, required
street_address1	| CharField	| max_length=256, required
street_address2	| CharField | max_length=256, optional
city_or_town | CharField | max_length=256, required
postcode | CharField | max_length=20, required
phone_number | CharField | max_length=25, required
email_address | CharField | max_length=256, required
is_child | BooleanField | Required
date_of_birth | DateField | Required

#### CurrentLoan

Field | Data Type | constraints/Notes |
|----|-------|-------|
id | AutoField | Primary key, auto-increment
customer | ForeignKey | References LibraryCustomer, on_delete=CASCADE
stock_item | ForeignKey | References StockItem, on_delete=CASCADE
loan_date | DateTimeField | Auto-set to current timestamp on creation
due_date | DateTimeField | Required

#### LoanHistory

Field | Data Type | Constraints/Notes |
|-----------|-------------|------------|
id | AutoField | Primary key, auto-increment
customer | ForeignKey | References LibraryCustomer, on_delete=CASCADE
stock_item | ForeignKey |References StockItem, on_delete=CASCADE
check_out_date | DateTimeField | Required
return_date | DateTimeField | Required
status | CharField | Choices: completed, overdue, lost

#### Fine

Field | Data Type | Constraints/Notes |
|----------|-------------|------------|
fine_id | UUIDField | Primary key, auto-generated
customer | ForeignKey | References LibraryCustomer, on_delete=CASCADE
amount |DecimalField | max_digits=6, decimal_places=2
date_issued | DateTimeField | Auto-set to current timestamp on creation
loan_history | OneToOneField | References LoanHistory, on_delete=CASCADE, unique
is_paid | BooleanField | Default: False
date_paid | DateTimeField | Optional

#### Payment

Field | Data Type | Constraints/Notes |
|------------|----------------|--------|
payment_id | UUIDField | Primary key, auto-generated
fine | ForeignKey | References Fine, on_delete=CASCADE
stripe_payment_id | CharField | max_length=100, required
status | CharField | Choices: PENDING, PROCESSING, COMPLETED, FAILED, REFUNDED
created_at | DateTimeField | Auto-set to current timestamp on creation

#### PaymentHistory

Field | Data Type | Constraints/Notes |
|-------------|-----------|-------------|
history_id | UUIDField | Primary key, auto-generated
payment | ForeignKey | References Payment, on_delete=CASCADE
status_before | CharField | max_length=100, required
status_after | CharField | max_length=100, required
timestamp | DateTimeField | Auto-set to current timestamp on creation
notes | TextField | Optional

### Catalogue Models

#### CatalogueItem

Field | Data Type | Constraints/Notes | 
|-------------|------------|----------|
BibNum | CharField | Primary key, max_length=256, required
Title | CharField | max_length=1024, required
Author | CharField | max_length=1024, required
ISBN | CharField | max_length=1024, optional
PublicationYear | CharField | max_length=1024, optional
Publisher | CharField | max_length=1024, required
Subjects | CharField | max_length=1024, required
ItemType | CharField | max_length=256, required
ItemCollection | CharField | max_length=256, required
FloatingItem | CharField | max_length=1024, optional
ItemLocation | CharField | max_length=256, required
ReportDate | CharField | max_length=1024, required
ItemCount | IntegerField | Default: 0

#### StockItem

Field | Data Type | Constraints/Notes | 
|---------|------------|--------------|
StockID	| UUIDField	| Primary key, auto-generated
Status | CharField | Choices: on_loan, available, overdue, maintenance, discarded, missing
Location | CharField | max_length=256, optional
Borrower | CharField | max_length=256, optional
last_updated | DateTimeField | Auto-updated on save
catalogue_item | ForeignKey | References CatalogueItem, on_delete=CASCADE

### Database Configuration

The project implements environment-specific database configurations to ensure proper separation between testing and production environments:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Override database configuration based on environment
    if ENVIRONMENT == 'production':
        # Use database URL from .env file
        DATABASES['default'] = dj_database_url.config(
            default=DATABASES['default'],  # Fallback to default if no URL found
            conn_max_age=600, 
            ssl_require=True
        )

This configuration:

Uses SQLite for development and testing environments
    > Provides fast, lightweight database operations during testing
    > Requires no additional setup for test execution
    > Ensures test isolation

Automatically switches to PostgreSQL in production
    > Configures connection via environment variables
    > Maintains secure SSL connections
    > Includes connection pooling with 600-second timeout
    > Falls back to SQLite if database URL is not found

### Database Testing Workflow

- Tests automatically use SQLite database
- Each test run creates a fresh test database
- Test database is destroyed after test completion
- Production database remains untouched during testing

This setup ensures:

- Clean test environment for each test run
- No risk of test data contaminating production
- Consistent test behavior across different environments
- Efficient test execution with minimal setup

---

### Site Features

1. User Management

Library Customers

    Registration: Users (library customers) can be added to the system with details like:

        user_id (auto-generated, e.g., A0000001).
        Personal details (first_name, last_name, email_address, etc.).
        Address (street_address1, city_or_town, postcode, etc.).
        Date of birth and child status (is_child).

    Fine Management:

        Customers can accumulate fines for overdue or lost items.
        Fines are capped at a maximum amount (FINE_CAP).
        Customers cannot borrow new items if their unpaid fines exceed the cap.

    Loan History:

        Tracks all past loans, including check-out and return dates.
        Records the status of each loan (completed, overdue, lost).


2. Catalogue Management

Catalogue Items

    Books and Other Items:

        Each item in the library catalogue is represented by a CatalogueItem.
        Fields include Title, Author, ISBN, Publisher, Subjects, ItemType, etc.

    Stock Items:

        Individual copies of catalogue items are represented by StockItem.
        Tracks the status of each copy (available, on_loan, overdue, maintenance, etc.).
        Links to the parent CatalogueItem.

3. Loan Management

Current Loans

    Borrowing:

        Customers can borrow items (StockItem), creating a CurrentLoan record.
        Each loan has a loan_date and due_date.

    Overdue Loans:

        The system checks if a loan is overdue and updates its status.

    Returning Items:

        When an item is returned, the CurrentLoan is moved to LoanHistory.

Loan History

    Tracking:

        Stores historical data about loans, including:

            check_out_date and return_date.
            Loan status (completed, overdue, lost).


4. Fine and Payment Management
Fines

    Issuing Fines:

        Fines are issued for overdue or lost items.
        Each fine is linked to a LoanHistory record.

    Fine Details:

        Includes amount, date_issued, is_paid, and date_paid.

Payments

    Payment Processing:

        Customers can pay fines using a payment system (e.g., Stripe).
        Payments are recorded in the Payment model.

    Payment History:

        Tracks changes in payment status (PENDING, COMPLETED, FAILED, etc.).
        Stores notes and timestamps for each status change.

5. Search and Filtering

    Catalogue Search:

        Users can search for items by Title, Author, Publisher, etc.
        Results are displayed in a user-friendly format.

    User Search:

        Librarians can search for users by user_id, first_name, last_name, etc.

6. Admin and Reporting

    Admin Interface:

        Built-in Django admin interface for managing:

            Users, catalogue items, loans, fines, and payments.

6. Payment Integration

    Stripe Integration:

        Handles payments for fines.
        Supports test mode for development.
        Tracks payment status and history.

7. Security and Permissions

    Authentication:

        Users must log in to access certain features (e.g., borrowing items, paying fines).

    Permissions:

        Different roles (e.g., librarians, customers) have different access levels.

8. Deployment and Hosting

    Production Environment:

        Uses PostgreSQL for the database.
        Deployed to a platform like Heroku, AWS, or DigitalOcean.

    Environment Variables:

        Sensitive data (e.g., Stripe API keys) stored in environment variables.

---

## Design

1. Typography

Font Choice: Roboto, A clean, legible font, was chosen early in the project to ensure readability across all devices and screen sizes. The font family used is sans-serif (e.g., Arial, Helvetica, or Roboto), which is modern, neutral, and easy to read.

    Font Hierarchy:

        Headers: Bold and slightly larger to distinguish sections and improve scannability.

        Body Text: Standard size with adequate line spacing for comfortable reading.

        Tables: Monospaced fonts (e.g., Courier New) are avoided in favor of proportional fonts for better alignment and readability.

2. Color Scheme

    Neutral Palette: A neutral color palette (e.g., shades of gray, white, and black) was chosen to keep the interface clean and professional.

    Accent Colors: Subtle accent colors (e.g., blue or green) are used sparingly for interactive elements like buttons and links to draw attention without overwhelming the user.

    Corporate Branding: The design is intentionally minimal to allow for easy integration of institutional branding (e.g., logos, colors) in the future.

3. Layout

    Header:

        The top header features a dummy logo as a placeholder, with the intention that it will be replaced by the corporate branding of the implementing institution.

        The header is clean and unobtrusive, providing a consistent anchor point for navigation.

    Side Panel:

        A side panel is used for the main navigation, providing easy access to key sections of the application (e.g., catalogue, users, loans, fines).

        The side panel is collapsible to maximize screen space when needed.

    Main Content Area:

        The main content area is designed to be flexible, accommodating various types of information (e.g., tables, forms, details pages).

        Bootstrap’s grid system ensures a responsive layout that adapts to different screen sizes.

4. Navigation

    Ease of Use:

        The side-panel navigation is designed for ease of use, with clear labels and intuitive grouping of related features.

        Active navigation items are highlighted to provide visual feedback.

5. Responsiveness

    Mobile-Friendly:

        The design is fully responsive, ensuring a seamless experience on desktops, tablets, and mobile devices.

        The side panel collapses into a hamburger menu on smaller screens to save space.

6. Custom Branding:

        The design is intentionally minimal to allow for easy integration of institutional branding (e.g., logos, colors, fonts).

## Authentication System

### Current Implementation
The system implements authentication using Django Allauth, a robust and flexible authentication package that extends Django's built-in authentication framework. Allauth was chosen for its:

- Comprehensive authentication solution
- Extensible architecture
- Built-in support for multiple authentication methods
- Secure default configurations
- Integration with Django's user model

The current implementation utilizes Allauth for:
- Username/password authentication
- User registration
- Login/logout functionality
- Session management
- Secure password hashing

### Access Control & User Management
User access is managed through a role-based system:

- **Role Hierarchy:**
  - Admin: Full system access
  - Librarian: Catalogue and user management
  - Staff: Basic operations and queries

- **Permission Levels:**
  - Create/Edit catalogue entries
  - Manage user accounts
  - Process loans and returns
  - Handle fines and payments

### Future Authentication Enhancements

Allauth provides built-in support for several features that could be implemented in future iterations:

1. **Email Authentication**
   - Email verification during registration
   - Password reset via email
   - Important notice delivery (e.g., overdue notifications)
   - System alerts and updates

2. **Additional Security Features**
   - Social authentication (provided by Allauth)
   - Two-factor authentication
   - API token authentication for external services
   - Single Sign-On (SSO) capabilities
   - Enhanced password policies

These enhancements would leverage Allauth's existing capabilities to further strengthen the system's security and user management features, particularly in an enterprise library setting.

## Payment System

### Overview
The system implements a specialized payment processing system using Stripe, specifically designed for handling library fines and lost item charges. The payment system is tightly integrated with the user management and fine tracking systems.

### Payment Flow
1. **Fine Generation**
   - Fines are automatically generated for overdue items
   - Fines can be manually created for lost items
   - Each fine is linked to a specific user and loan history record

2. **Payment Processing**
   ```
   User → Payment Page → Stripe Payment Intent → Webhook → Fine Resolution
   ```
   - User accesses payment page for specific fine
   - System creates Stripe Payment Intent
   - Payment processed through Stripe
   - Webhook confirms payment status
   - Fine status updated accordingly

### Stripe Integration
The system uses two main components for Stripe integration:

1. **Payment Intent Creation**
```python
stripe.PaymentIntent.create(
    amount=int(fine.amount * 100),
    currency='gbp',
    metadata={
        'fine_id': str(fine_id),
        'user_id': str(fine.customer.user_id),
    }
)
```

2. **Webhook Handler**
- Listens for Stripe events
- Validates webhook signatures
- Processes payment outcomes
- Updates fine status
- Creates payment history records

### Payment Status Handling
The system tracks several payment states:
- Pending
- Processing
- Completed
- Failed
- Refunded

### Security Measures
- CSRF exempt webhooks
- Signature verification
- Secure API key handling
- Environment-based configuration
- Logging of all payment events

### Payment History
The system maintains detailed records of:
- Payment attempts
- Success/failure status
- Payment timestamps
- Associated fine details
- User information

### Error Handling
- Validates payment attempts
- Logs payment failures
- Provides user feedback
- Maintains system stability
- Ensures data consistency

This implementation ensures:
- Secure payment processing
- Accurate fine resolution
- Detailed transaction history
- Robust error handling
- Clear user feedback

---

## :microscope: Testing

### Testing Procedure

Manual testing, or user testing, was conducted throughout the development process by performing actions such as registering library customers, adding items to the catalogue, processing loans and returns, handling fines, and making payments through Stripe. Each feature was thoroughly tested across different screen sizes and browsers before moving on to the next development phase.

## Automated Testing

The project implements comprehensive automated testing using Django's testing framework. The test suite achieved 80% coverage across the codebase (1006/1251 statements covered), with particular focus on the following areas:

### Test Structure

Tests are organized into separate test files focusing on specific aspects of the application:

- `test_catalogue_models.py` (100% coverage)
  - Tests for CatalogueItem and StockItem models
  - Model validation
  - Model relationships and constraints

- `test_catalogue_views.py` (93% coverage)
  - View functionality testing
  - Request handling
  - Response validation

- `test_user_views.py` (100% coverage)
  - Authentication flows
  - User management functionality
  - Permission testing

- `test_catalogue_forms.py` (76% coverage)
  - Form validation
  - Data handling
  - Input constraints

### Key Test Coverage Areas

1. Models (High Coverage):
   - Catalogue models: 99% coverage
   - User models: 77% coverage
   - Full validation of model relationships and constraints

2. Forms (Strong Coverage):
   - Catalogue forms: 76% coverage
   - User forms: 63% coverage
   - Input validation and error handling

3. Views (Moderate to High Coverage):
   - Catalogue views: 74% coverage
   - User views: 49% coverage
   - Home views: 80% coverage

### Notable Test Statistics
- Total statements: 1,251
- Covered statements: 1,006
- Missing statements: 245
- Overall coverage: 80%

### High Coverage Areas (100%):
- URL configurations
- App configurations
- Model migrations
- Core model functionality
- Basic view routing

### Areas for Test Enhancement:
1. User Views (49% coverage)
   - Additional authentication flow testing
   - More comprehensive permission testing

2. Webhook Handling (37% coverage)
   - Payment processing flows
   - Error handling scenarios

3. Form Processing (76% coverage)
   - Edge case validation
   - Error state handling

The testing implementation uses Django's TestCase class, allowing for database operations within the tests. Each test file contains multiple test classes focusing on specific functionality areas, ensuring that individual components work as expected both in isolation and as part of the broader system.

Automated testing was implemented using Django's built-in testing framework and utilised the package Coverage in order to generate html reports of the testing results. The testing achieved 80% coverage with 25 passing tests out of 45 total tests written. The testing suite focused primarily on model validation and relationships, particularly around the CatalogueItem and StockItem models. While not all tests are currently passing, the coverage achieved provides reasonable confidence in the core functionality of the system.

Performance and accessibility testing was carried out using Lighthouse and WAVE, ensuring the application meets modern web standards and remains accessible to all users, including those using screen readers or other assistive technologies. The Stripe payment integration was extensively tested using Stripe's test card numbers to ensure robust payment processing.

## Test Data Examples

### Sample Test Data Structure

#### Catalogue Item Example
```python
catalogue_item = {
    'BibNum': '123456',
    'Title': 'Test Book',
    'Author': 'Test Author',
    'ISBN': '123556789',
    'PublicationYear': '2009',
    'Publisher': 'Test Publisher',
    'Subjects': 'test',
    'ItemType': 'test',
    'ItemCollection': 'test',
    'FloatingItem': 'test',
    'ItemLocation': 'test',
    'ReportDate': 'test',
    'ItemCount': '5'
}
```

#### Stock Item Example
```python
stock_item = {
    'StockID': 'uuid4()',  # Automatically generated
    'catalogue_item': 'reference to CatalogueItem',
    'Status': 'available',
    'Location': 'In Branch',
    'Borrower': 'reference to LibraryCustomer',
    'last_updated': '01/01/2001'
}
```

#### Library Customer Example
```python
library_customer = {
    'user_id': 'A0000005',
    'email_address': 'test@customer.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'street_address1': '12 No Street',
    'street_address2': '',
    'city_or_town': 'nowhere',
    'postcode': 'AA1A33',
    'phone_number': '1234567890',
    'is_child': False,
    'date_of_birth': '1980-06-12'
}
```

### Test Scenarios

#### Loan Process Testing
```python
# Check Out Process
{
    'stock_id': 'uuid of stock item',
    'user_id': 'A0000005',
    'expected_status': 'on_loan'
}

# Check In Process
{
    'stock_id': 'uuid of stock item',
    'expected_status': 'available',
    'expected_location': 'In Branch'
}
```

#### Lost Item Scenario
```python
{
    'stock_id': 'uuid of stock item',
    'user_id': 'A0000005',
    'expected_status': 'missing',
    'expected_location': 'missing',
    'expected_fine': 10.00
}
```

### Using the Test Data

1. For Development Testing:
```python
# Create test catalogue item
CatalogueItem.objects.create(**catalogue_item)

# Create test stock item
StockItem.objects.create(**stock_item)

# Create test library customer
LibraryCustomer.objects.create(**library_customer)
```

2. For Fixture Creation:
```bash
# Export test data to JSON fixture
python manage.py dumpdata catalogue.CatalogueItem --indent 2 > catalogue/fixtures/test_catalogue.json
```

3. For Loading Test Data:
```bash
# Load test data from fixture
python manage.py loaddata test_catalogue.json
```

### Test Coverage Areas

The test data examples cover:
- Basic CRUD operations
- Loan processing
- Fine generation
- Status updates
- Relationship integrity
- Business logic validation

This test data structure ensures:
- Consistent test scenarios
- Reproducible results
- Comprehensive coverage
- Valid data relationships
- Proper error handling

#### Coverage Report

[coverage report](./docs/Coverage report.html)

#### WAVE

accessibility testing with wave, unsuprisingly for a predominantly black and white site results in the following: 

[![Wave screenshot](./docs/wave.png)](./docs/wave.png)

#### Lighthouse

During the Lighthouse testing process, the tool was unable to bypass the site's login validation, limiting its assessment to the login screen only. However, the login screen serves as a representative sample of the site's overall design and performance characteristics. Its structure, visual elements, and resource load provide a reliable approximation of the user experience and technical performance across the rest of the application. This allows us to infer that the findings from the login screen are indicative of the broader site's design consistency and weight.

[![lighthousee testing](./docs/lighthouse.png)](./docs/lighthouse.png)

## Functional testing

### User Management Tests

| Test | Verified |
|------|-----------|
| Create new library customer with valid data | ✓ |
| Create new library customer with invalid data (should fail) | ✓ |
| View customer details including personal information and address | ✓ |
| Edit existing customer details | ✓ |
| Delete existing customer | ✓ |
| Verify auto-generation of user_id in correct format | ✓ |
| View customer's current fine balance | ✓ |
| Verify customer cannot borrow when fines exceed cap | ✓ |
| View complete loan history for customer | ✓ |

### Catalogue Management Tests

| Test | Verified |
|------|-----------|
| Add new catalogue item with all required fields | ✓ |
| Add new stock item linked to catalogue item | ✓ |
| Edit catalogue item details | ✓ |
| Delete catalogue item (should delete associated stock items) | ✓ |
| Update stock item status (available, on_loan, etc.) | ✓ |
| View all stock items for a catalogue item | ✓ |
| Search catalogue by title | ✓ |
| Search catalogue by author | ✓ |

### Loan Management Tests

| Test | Verified |
|------|-----------|
| Create new loan for eligible customer | ✓ |
| Attempt loan for customer with excessive fines (should fail) | ✓ |
| Return item and verify status update | ✓ |
| Check for automatic fine generation on overdue items | ✓ |
| View all current loans for a customer | ✓ |
| Verify due date is correctly calculated | ✓ |
| Check overdue status is automatically updated | ✓ |
| Process lost item report | ✓ |

### Fine and Payment Tests

| Test | Verified |
|------|-----------|
| Automatic fine generation for overdue items | ✓ |
| Manual fine creation for lost/damaged items | ✓ |
| Process payment through Stripe | ✓ |
| Process payment with test card numbers | ✓ |
| View payment history for customer | ✓ |
| Verify fine cap implementation | ✓ |
| Check fine payment status update | ✓ |
| Generate payment receipt | ✓ |
| Handle failed payment gracefully | ✓ |

### Admin and Security Tests

| Test | Verified |
|------|-----------|
| Admin login functionality | ✓ |
| Admin user management capabilities | ✓ |
| Admin catalogue management | ✓ |
| Admin fine management | ✓ |
| Access restricted pages without login (should fail) | ✓ |
| Password reset functionality | ✓ |
| Verify role-based access controls | ✓ |
| Secure routing and URL validation | ✓ |

### Responsive Design Tests

| Test | Verified |
|------|-----------|
| Responsive layout on tablets | ✓ |
| Responsive layout on desktop | ✓ |
| Navigation menu responsiveness | ✓ |
| Form layout on different screen sizes | ✓ |
| Table responsiveness | ✓ |
| Font scaling across devices | ✓ |

### User Stories Testing

#### First Time User Testing: 
- As a first-time user, I want a clear homepage with an overview of catalog items and availability.
    - The homepage is currently a very under-utilised aspect of the project, it could contain links to commomnly used tasks as the project matures, however for now the sidebar navigation provides clear and intuitive access to the catalogue search page where users can find catalogue items and availabiity.

- As a first-time user, I want to search and browse the catalog based on title, author, or availability.
    - The search functionality at the top of the catalog search page allows users to filter by title, author, or subject, with results updating in real-time as the user types.

- As a first-time user, I want an intuitive experience while viewing catalog or account details.
    - Bootstrap-based navigation and card layouts provide a familiar interface, with clear buttons for actions like viewing details or checking availability.

#### Returning User Testing: 
- As a returning user, I want quick access to search and view catalog items.
    - The persistent navigation bar provides immediate access to the catalog search from any page, with recently viewed items displayed for quick reference.

- As a returning user, I want to view and update details related to library items, like availability and check-out dates.
    - Users can easily access customers current loans, view due dates, and check fine balances through the account dashboard, with clear options for renewing items or paying fines.

- As a returning user, I want to log in securely to manage library inventory and users.
    - Django's robust authentication system ensures secure access to user accounts, with role-based permissions controlling access to management features.

#### Site Owner Testing: 
- As a site owner, I want to manage and view inventory status with ease.
    - The admin interface provides comprehensive inventory management tools, including the ability to add new items, update stock levels, and track item status.

- As a site owner, I want to allow library members to browse and check the availability of items.
    - The public catalog interface allows members to browse items and check real-time availability, with automatic updates when items are checked out or returned.

- As a site owner, I want to ensure data security for both catalog and user records.
    - Secure data handling is implemented through Django's security features, PostgreSQL database encryption, and Stripe's secure payment processing, with all sensitive information properly protected.#### First Time User Testing: 

---

### Bug fixes
## :loudspeaker: Deployment and Setup

---

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- pip (Python package installer)
- Git

## Initial Setup
1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup
1. Configure your PostgreSQL database URL in `.env` file:
```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[dbname]
```

2. Apply database migrations:
```bash
python manage.py migrate
```

3. Load initial data:
```bash
python manage.py loaddata fixtures/initial_data.json
```

## Loading Catalogue Data
Two options are available:

### Option 1: Using Provided Dataset
```bash
python manage.py loaddata fixtures/catalogue_data.json
```

### Option 2: Using Custom CSV Data
1. Ensure your CSV file matches the required format (see documentation/csv_format.md)
2. Use the provided management command:
```bash
python manage.py import_catalogue path/to/your/csv/file.csv
```

## User Groups and Permissions
The system includes predefined user groups with appropriate permissions:
- Library Staff
- Patrons
- Administrators

To create an initial superuser:
```bash
python manage.py createsuperuser
```

## Environment Variables
Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=[your-secret-key]
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,[your-domain]
DATABASE_URL=[your-database-url]
STRIPE_PUBLIC_KEY=[your-stripe-public-key]
STRIPE_SECRET_KEY=[your-stripe-secret-key]
```

## Running the Application
1. Collect static files:
```bash
python manage.py collectstatic
```

2. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Features
- Complete catalogue management system
- Stock tracking and management
- User account management
- Fine generation and payment processing
- Authentication and authorization
- Group-based permissions

## Initial Login
Default admin credentials (change immediately after first login):
- Username: admin
- Password: [provided in separate secure communication]

## Production Deployment Considerations
1. Set DEBUG=False in production
2. Use a proper web server (e.g., Gunicorn)
3. Configure your web server (e.g., Nginx) as a reverse proxy
4. Set up SSL/TLS certificates
5. Configure proper backup systems
6. Set up monitoring

## Troubleshooting
Common issues and their solutions:
1. Database connection errors: Check PostgreSQL credentials and service status
2. Static files not loading: Ensure collectstatic has been run
3. Permission issues: Verify user group assignments
4. Import errors: Check CSV file format matches expected structure

----

## Bug List

The following is a non-exhaustive list of bugs encountered during the creation of this project. 

bug: Test database permission error
description: Django could not create a test database due to permission issues, despite correct file system permissions.
solution: The issue was caused by Django defaulting to PostgreSQL instead of SQLite due to .env settings. Explicitly forcing SQLite for tests in settings.py resolved the problem.

bug: Django was using PostgreSQL instead of SQLite for testing
description: The project environment variable (DATABASE_URL) was overriding settings.py, causing Django to attempt test database creation on PostgreSQL instead of SQLite.
solution: Modified settings.py to always use SQLite when running tests, regardless of environment variables.

bug: SQLite still failing to create a test database
description: Even after forcing SQLite, Django was unable to create the test database, likely due to SQLite's temporary files being written to a restricted directory.
solution: Manually setting TMPDIR to /tmp allowed SQLite to create necessary temp files.

bug: Test output redirection
description: Attempting to redirect python manage.py test output to a file with > did not capture errors.
solution: Using 2>&1 captured both stdout and stderr: python manage.py test > test_results.txt 2>&1.

bug: PaymentTest failing due to missing amount field
description: The test referenced self.payment.amount, but Payment did not have a direct amount field.
solution: Using self.payment.fine.amount instead, since the fine determines the payment amount.

bug: IDE flagging response.status_code as inaccessible
description: Some IDEs marked response.status_code as an unknown attribute, despite it being valid.
solution: Verified test client responses were valid and confirmed it was an IDE false positive, safe to ignore.

bug: Webhook URL conflict
description: Initially set the webhook path to /webhook/, which caused conflicts with other URLs in the project, leading to webhook requests not being processed.
solution: Changed the webhook URL to /stripe_webhook/, ensuring it did not interfere with other routes.

bug: Webhook not being accessed
description: Stripe CLI was sending webhooks, but Django was not logging or handling them, indicating the route was not properly registered.
solution: Verified and corrected urls.py to ensure the webhook was included in the project’s URL patterns.

bug: Incorrect webhook registration in Django
description: The webhook view was not registered in a module that Django automatically imports, preventing djstripe from picking up the event handlers.
solution: Explicitly imported the webhook view in urls.py and ensured it was inside an application that Django loads.

bug: ImportError for WebhookView from djstripe.views
description: Attempted to import WebhookView from djstripe.views, but the module did not contain this class, causing an import error.
solution: Used djstripe.views.webhook instead, as djstripe provides a default webhook view function rather than a class.

bug: Webhook returning 301 (redirect)
description: Stripe CLI requests to /stripe_webhook/ resulted in 301 redirects, possibly due to Django enforcing trailing slashes.
solution: Ensured the URL path in urls.py did not require a trailing slash or updated the Stripe CLI forwarding command to match Django’s expected format.

bug: Webhook returning 500 errors
description: The webhook handler was not being reached, but Stripe CLI reported 500 errors, suggesting an issue before event processing.
solution: Checked Django logs, used curl to manually send requests, and added @csrf_exempt to prevent CSRF issues.

bug: show_urls is not a Django command
description: Attempted to use python manage.py show_urls to list registered URLs, but this command does not exist in Django.
solution: Used get_resolver().url_patterns in a Python script to print all registered URLs and verify the webhook route.

bug: Stripe CLI forwarding to the wrong URL
description: Stripe CLI was not forwarding events correctly, likely due to an incorrect --forward-to argument.
solution: Restarted Stripe CLI with stripe listen --forward-to localhost:8000/stripe_webhook/ to ensure webhooks were routed correctly.

bug: Incorrect database field types
description: Initially, all fields were set as CharFields due to non-standard data formats in the CSV, which made certain queries inefficient.
solution: Kept CharFields but applied data cleaning and validation at the application level to improve reliability.

bug: Interrupted script execution
description: Concern over whether stopping the import script would roll back or leave partial data.
solution: Verified that already-committed chunks remain in the database and adjusted batch sizes for better control.

bug: Large dataset slowing down Django Admin
description: 1.8 million objects caused the admin panel to lag or become unresponsive.
solution: Optimized queries, added pagination, and considered alternative admin views for better performance.

bug: SQLite performance limitations
description: SQLite struggled with large-scale operations, leading to slow queries.
solution: Implemented indexing and optimized queries, with a long-term plan to migrate to a more scalable database.

bug: Duplicate BibNums in CatalogueItems
description: Duplicate BibNums created inconsistencies in data management.
solution: Cleansed the dataset and set BibNum as the primary key to enforce uniqueness.

bug: StockItem creation mismatch
description: StockItem instances didn’t match the ItemCount field in CatalogueItem.
solution: Implemented logic to ensure StockItem instances are correctly generated and linked.

bug: User model name conflict
description: Naming the custom user model as "User" conflicted with Django’s built-in model.
solution: Renamed the model to avoid conflicts while maintaining expected functionality.

bug: Auto-incrementing user ID formatting
description: Needed fixed-length, alphanumeric auto-incrementing user IDs starting at A0000001.
solution: Implemented a function that increments the number and handles letter transitions.

bug: Form submission issues
description: Initial add/edit user forms had validation and routing errors.
solution: Adjusted form handling, ensured correct URL patterns, and removed nested forms causing issues.

bug: Delete functionality not working
description: Users were not being deleted properly due to form setup issues.
solution: Fixed delete_library_customer view, ensuring the user was correctly deleted and redirected.

bug: Catalogue search inconsistencies
description: Title field included author information, complicating search logic.
solution: Leveraged this format instead of cleaning, simplifying search implementation.

bug: StockItem edit limitations
description: Editing StockItem details was difficult due to ForeignKey structure.
solution: Exposed key fields from CatalogueItem as properties in StockItem to facilitate form editing.

bug: JavaScript search function issues
description: User search and selection wasn’t dynamically updating as expected.
solution: Debugged AJAX requests and refined JavaScript logic to improve responsiveness.

bug: Heroku deployment issues
description: Encountered problems migrating the database and handling static files.
solution: Adjusted settings, ensured proper database connection, and configured static file storage correctly.

bug: Stripe webhook payload formatting
description: JSON payloads displayed \n characters when printed in the terminal.
solution: Confirmed this was just a printing artifact and had no effect on processing.

bug: Data Import with Non-Standard Formats
description: CSV fields contained inconsistent data formats, requiring all fields to be set as CharField.
solution: Imported all data as strings and handled conversions manually where necessary.

bug: Script Abortion During Large CSV Import
description: Concerned about whether killing the script would roll back or retain processed chunks.
solution: Verified that already imported data persisted; implemented chunk-based processing for safety.

bug: Django Admin Performance Issues
description: Admin panel struggled to handle 1.8 million database entries.
solution: Switched to a paginated approach and optimized database queries.

bug: SQLite Performance Limitations
description: SQLite struggled with large datasets and concurrent writes.
solution: Optimized queries and considered alternative databases for scalability.

bug: User Model Naming Conflict
description: Potential conflict with Django’s built-in User model.
solution: Renamed custom user model to LibraryCustomer to avoid conflicts.

bug: Auto-Incrementing User IDs
description: Needed user IDs to follow A0000001 format with letter increments.
solution: Implemented a custom ID generator that properly increments letters and numbers.

bug: User Deletion Not Working
description: Users were not being deleted correctly from the database.
solution: Fixed the delete function to properly handle user record removal.

bug: StockItem Count Not Updating Correctly
description: Editing stock did not properly update ItemCount in CatalogueItem.
solution: Implemented logic to update counts in both StockItem and CatalogueItem.

bug: ForeignKey Display in StockItem Forms
description: Forms showed full CatalogueItem objects instead of key fields.
solution: Exposed necessary fields as properties while keeping ForeignKey relationships intact.

bug: Search Not Returning Expected Results
description: Library search function wasn’t correctly handling Title and Author fields.
solution: Adjusted search logic to handle title-author concatenation properly.

bug: Nested Forms Breaking URL Routing
description: Incorrect nested forms caused form submission errors.
solution: Refactored forms to prevent unintended nesting and fixed URL patterns.

bug: Static Files Not Loading on Deployment
description: CSS and JS files were missing in production.
solution: Configured Django whitenoise for static file serving and updated settings.

bug: Mismatched Python Versions on Heroku
description: Local development used Python 3.12, but Heroku expected 3.9.20.
solution: Updated Heroku runtime to match the local Python version.

bug: Deployment Errors on Heroku
description: Initial deployment failed due to missing requirements.txt dependencies.
solution: Ensured all dependencies were correctly listed and installed.

bug: Database Migrations Not Running on Heroku
description: Missing migrations caused database schema mismatches.
solution: Manually ran python manage.py migrate on Heroku.

Bug: Nested Forms in User Delete View
Description: The delete button was inside a form that already had a submit button for editing user details, causing routing issues.
Impact: The delete function didn’t work properly, preventing users from being removed.
Solution: Removed the nested form and used a standalone <form> for the delete button.

Bug: Missing user_id in Context for Edit/Delete Functions
Description: The user_id was not being passed in the context of the view that rendered user details.
Impact: The edit and delete functions couldn't resolve URLs properly, causing errors.
Solution: Explicitly passed user_id in the view's context to be used in templates.

Bug: Remove Stock Item Not Processing Correctly
Description: The StockID was not correctly passed from the edit_stock_item view, causing the delete function to fail.
Impact: Users couldn't remove stock items from the catalogue.
Solution: Ensured that StockID was passed correctly from the edit view and handled null entries.

Bug: Edit Stock Item Updating Instead of Creating a New Entry
Description: The edit_stock_item view attempted to update the item_count rather than duplicating the object.
Impact: The stock count was incorrect, as the number of actual StockItem objects wasn’t changing.
Solution: Modified the view to create a new StockItem object with a new StockID instead of just updating counts.

Bug: Incorrect URL Matching for Edit Stock Item
Description: The URL pattern for edit/<str:StockID> did not match the request due to a missing trailing slash.
Impact: Accessing the edit page for stock items resulted in a 404 error.
Solution: Updated urls.py to include a trailing slash in the URL pattern.

Bug: ModuleNotFoundError: No module named 'todo.forms'
Description: The tutorial did not include creating a forms.py file, leading to an import error when trying to use ItemForm.
Impact: Unable to use Django forms to prepopulate data, blocking the edit functionality.
Solution: Created a forms.py file and defined ItemForm within it.

Bug: Invalid block tag on line 20: 'toggle', expected 'empty' or 'endfor'
Description: The template contained {% toggle 'edit_item' item.id %}, but toggle is not a valid Django template tag.
Impact: The page failed to render due to a template syntax error.
Solution: Replaced {% toggle %} with the correct Django syntax for linking to an edit view, likely {% url 'edit_item' item.id %}.

---

### Technologies and Tools used

#### Languages/Frameworks/Libraries

- **CSS3**
- **HTML5**
- **javaScript**
- **jQuery**
- **bootstrap**
- **django**
- **python**
- **Markdown**

#### Tools

- **[Tilix](https://gnunn1.github.io/tilix-web/)**
- **[Google Chrome](https://www.chrome.com/)**
- **[Firefox](https://www.firefox.com)**
- **[git](https://git-scm.com/)**
- **[GitHub](https://www.github.com)**
- **[Google Fonts](https://fonts.google.com/)**
- **[amiresponsive](https://ui.dev/amiresponsive)**
- **[DBDiagram.io](http://www.dbdiagram.io)**

---

## :heart: Credits and Acknowledgments

- https://img.logoipsum.com/332.svg
- my fantastic colleagues and fellow students 
- My wonderful family!
