

CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    `date` DATE NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

DROP TABLE `Entries`;

INSERT INTO `Entries` VALUES (null, "Javascript", "I learned about loops today. They can be a lot of fun.", 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entries` VALUES (null, "here is a concept", "here is an entry", 2, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entries` VALUES (null, "here is another concept", "here is another entry", 3, "Wed Sep 15 2021 10:10:47 ");

SELECT * FROM Entries;

SELECT * 
FROM Entries
WHERE entry LIKE '%from%';

ALTER TABLE JournalEntries RENAME TO Entries;


CREATE Table `Moods` (
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`label` TEXT NOT NULL
);

INSERT INTO Moods VALUES (null, "Happy")
INSERT INTO Moods VALUES (null, "Sad")
INSERT INTO Moods VALUES (null, "Perplexed")


SELECT * FROM Moods;





CREATE Table `Tags` (
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`name` TEXT NOT NULL
)

INSERT INTO Tags VALUES (null, "Ideas");
INSERT INTO Tags VALUES (null, "Projects");
INSERT INTO Tags VALUES (null, "Personal");

SELECT * FROM Tags



CREATE Table `EntryTags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `journal_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`journal_id`) REFERENCES `Entries`(`id`)
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
)


INSERT INTO `EntryTags` VALUES (null, 1, 1);
INSERT INTO `EntryTags` VALUES (null, 2, 2);
INSERT INTO `EntryTags` VALUES (null, 3, 3);

SELECT * FROM EntryTags
