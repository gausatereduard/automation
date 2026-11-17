<?php

declare(strict_types=1);

require_once __DIR__ . '/src/Site.php';

$currentPage = 'index.php';
$pageHeading = page_title($currentPage);

require __DIR__ . '/includes/header.php';
?>
<main class="container">
    <section class="hero">
        <p class="eyebrow">Lab 05 &middot; Jenkins + Ansible</p>
        <h1>Configure once, deploy anywhere.</h1>
        <p class="lead">
            This small static website is the deployment target for the lab 05 pipeline.
            Jenkins builds and tests it on an SSH agent, Ansible configures the test
            server, and a second pipeline publishes this page.
        </p>
        <div class="actions">
            <a class="button" href="about.php">Learn more</a>
            <a class="button button--ghost" href="contact.php">Get in touch</a>
        </div>
    </section>

    <section class="cards" aria-label="Site highlights">
        <article class="card">
            <h2>Plain PHP</h2>
            <p>No framework and no database. A few PHP templates and one small helper library.</p>
        </article>
        <article class="card">
            <h2>Tested in CI</h2>
            <p>The helper library is covered by PHPUnit tests that run on the Jenkins SSH agent.</p>
        </article>
        <article class="card">
            <h2>Configured by Ansible</h2>
            <p>Apache, PHP and the virtual host are installed and managed by an Ansible playbook.</p>
        </article>
    </section>

    <section class="note">
        <h2>What the pipelines do</h2>
        <ol class="steps">
            <li>Clone the repository and install the development dependencies with Composer.</li>
            <li>Run the PHPUnit test suite and publish the JUnit report.</li>
            <li>Configure the Ubuntu test server with Apache and PHP.</li>
            <li>Copy the site to the test server and verify that it responds.</li>
        </ol>
    </section>
</main>
<?php require __DIR__ . '/includes/footer.php'; ?>
