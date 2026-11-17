<?php

declare(strict_types=1);

require_once __DIR__ . '/src/Site.php';

$currentPage = 'about.php';
$pageHeading = page_title($currentPage);

require __DIR__ . '/includes/header.php';
?>
<main class="container">
    <section class="page-head">
        <p class="eyebrow">About</p>
        <h1><?= e($pageHeading) ?></h1>
        <p class="lead">
            Aurora Studio exists only as a realistic-looking artefact for a university
            automation lab. It is deliberately simple so the focus stays on Jenkins and Ansible.
        </p>
    </section>

    <section class="prose">
        <h2>How it is built</h2>
        <p>
            Every page is a plain PHP file. Shared markup lives in <code>includes/header.php</code>
            and <code>includes/footer.php</code>, while the small helper library in
            <code>src/Site.php</code> provides the title, navigation and formatting functions.
            The stylesheet is a single static file.
        </p>

        <h2>What it is used for</h2>
        <ul>
            <li>The Jenkins build pipeline installs its Composer dependencies and runs PHPUnit.</li>
            <li>The Ansible playbook installs Apache2 and PHP on an Ubuntu container.</li>
            <li>The deploy pipeline copies these files to <code>/var/www/html</code> on the test server.</li>
        </ul>

        <h2>Technology</h2>
        <ul class="tags">
            <li>PHP 8</li>
            <li>Apache 2</li>
            <li>PHPUnit</li>
            <li>Docker Compose</li>
            <li>Jenkins</li>
            <li>Ansible</li>
        </ul>
    </section>
</main>
<?php require __DIR__ . '/includes/footer.php'; ?>
