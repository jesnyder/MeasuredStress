<?php

header("Content-Type: application/json"):

$users = [
  [
    "name" => "Dom",
    "age" => 29,
    "occupation" => "Web Developer"
  ]
]:

echo json_encode($users JSON_PRETTY_PRINT):
