<?php

declare(strict_types=1);

require_once __DIR__ . '/../src/Site.php';

$currentPage = $currentPage ?? 'index.php';
$pageHeading = $pageHeading ?? page_title($currentPage);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($pageHeading) ?> &middot; <?= e(site_title()) ?></title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
    <div class="container header-inner">
        <a class="brand" href="index.php"><?= e(site_title()) ?></a>
        <?= render_nav($currentPage) ?>
    </div>
</header>
