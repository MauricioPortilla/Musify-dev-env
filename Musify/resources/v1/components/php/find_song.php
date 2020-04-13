#!/usr/local/bin/php

<?php

$songsDirectory = __DIR__ . "/../../../../storage/songs";
$songFormats = ["wav", "mp3"];
$songId = $argv[1];

foreach (new DirectoryIterator($songsDirectory) as $iterator) {
    if ($iterator->isDot()) {
        continue;
    } elseif ($iterator->isFile()) {
        foreach ($songFormats as $songFormat) {
            if ($iterator->getBasename("." . $songFormat) == $songId) {
                echo $iterator->getBasename();
                return;
            }
        }
    }
}

?>
