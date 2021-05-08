CREATE TABLE IF NOT EXISTS Login (
utorid NVARCHAR (30) PRIMARY KEY NOT NULL,
password NVARCHAR (50) NOT NULL,
position NVARCHAR (11) NOT NULL,
name NVARCHAR (30) NOT NULL
);

INSERT INTO login VALUES('student1', 'student1', 'student', 'Sarah Johnson');
INSERT INTO login VALUES('student2', 'student2', 'student', 'Alduin Sorano');
INSERT INTO login VALUES('instructor1', 'instructor1', 'instructor', 'George Burd');
INSERT INTO login VALUES('instructor2', 'instructor2', 'instructor', 'Stephanie Goldberg');

CREATE TABLE IF NOT EXISTS Grades (
utorid NVARCHAR (30) NOT NULL,
name NVARCHAR (30) NOT NULL,
assessments NVARCHAR (30) NOT NULL,
grade INTEGER NOT NULL,
FOREIGN KEY(utorid) REFERENCES Login(utorid),
PRIMARY KEY(utorid, assessments)
);

INSERT INTO grades VALUES('student1', 'Sarah Johnson', 'Midterm', 80);
INSERT INTO grades VALUES('student1', 'Sarah Johnson', 'Assignment1', 30);
INSERT INTO grades VALUES('student2', 'Alduin Sorano', 'Assignment1', 90);

CREATE TABLE IF NOT EXISTS Regrade (
utorid NVARCHAR (30) NOT NULL,
name NVARCHAR (30) NOT NULL,
assessments NVARCHAR (30) NOT NULL,
reason NVARCHAR (250),
FOREIGN KEY(utorid) REFERENCES Login(utorid),
FOREIGN KEY(name) REFERENCES Login(name),
FOREIGN KEY(assessments) REFERENCES Grades(assessments),
PRIMARY KEY(utorid, assessments)
);

INSERT INTO regrade VALUES('student1', 'Sarah Johnson', 'Midterm', 'Q1 marks should not be taken off');
INSERT INTO regrade VALUES('student2', 'Alduin Sorano', 'Assignment1', 'Wrong mark given for Q4');

CREATE TABLE IF NOT EXISTS Anonfeedback (
utorid NVARCHAR (30) NOT NULL,
answer1 NVARCHAR (250),
answer2 NVARCHAR (250),
answer3 NVARCHAR (250),
answer4 NVARCHAR (250),
FOREIGN KEY(utorid) REFERENCES Login(utorid)
);

INSERT INTO anonfeedback VALUES('instructor1', 'A1','A2','A3','A4');
INSERT INTO anonfeedback VALUES('instructor1', 'B1','B2','B3','B4');
INSERT INTO anonfeedback VALUES('instructor2', 'C1','C2','C3','C4');
