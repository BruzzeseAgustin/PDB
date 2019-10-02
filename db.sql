-- Create a new database called 'pdb'
-- Connect to the 'master' database to run this snippet
USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
    SELECT name
        FROM sys.databases
        WHERE name = N'pdb'
)
CREATE DATABASE pdb;
USE pdb;

CREATE TABLE pages (
    id
    BIGINT(7) not NULL AUTO_INCREMENT,
    title VARCHAR(200),
    content VARCHAR(10000),
    url VARCHAR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

INSERT INTO pages (title, content, url) VALUES("Test page title","this is some test page content. It can be up to 10,000 characters long", "https://github.com/BruzzeseAgustin");
ALTER DATABASE pdb CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE pages CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE pages CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE pages CHANGE url url VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

DESCRIBE pages; 