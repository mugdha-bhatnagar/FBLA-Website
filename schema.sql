-- right click and run query to make the tables work
-- Use the elemental position of the stuff in the array for the table
--Table: jobs
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    distance INTEGER NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT 0
);
INSERT INTO jobs(title, company, distance)
VALUES ("Software Intern", "TechCorp", 5);
--VALUES ("Graphic Designer",  "DesignHub",10);



-- Table: students
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Table: applications
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    job_id INTEGER,
    applied_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);

-- Table: bookmarks
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    job_id INTEGER,
    bookmarked_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);

-- Table: letters_of_rec (letters of recommendation)
CREATE TABLE letters_of_rec (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    professor_name TEXT NOT NULL,
    content TEXT NOT NULL,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(id)
);


-- ALTER TABLE applications ADD COLUMN status TEXT DEFAULT 'Pending';

SELECT * FROM jobs;
