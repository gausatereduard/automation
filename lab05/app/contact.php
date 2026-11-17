<?php

declare(strict_types=1);

require_once __DIR__ . '/src/Site.php';

$currentPage = 'contact.php';
$pageHeading = page_title($currentPage);

require __DIR__ . '/includes/header.php';
?>
<main class="container">
    <section class="page-head">
        <p class="eyebrow">Contact</p>
        <h1><?= e($pageHeading) ?></h1>
        <p class="lead">This page is static: there is no form handler and nothing is stored on the server.</p>
    </section>

    <section class="contact-grid">
        <article class="card">
            <h2>Email</h2>
            <p><a href="mailto:hello@example.com">hello@example.com</a></p>
            <p class="muted">Answers are not guaranteed — this is a lab project.</p>
        </article>

        <article class="card">
            <h2>Location</h2>
            <p>Test server inside the Docker network</p>
            <p class="muted">Host: <code>test-server</code> &middot; Port: <code>80</code></p>
        </article>

        <article class="card">
            <h2>Deployed on</h2>
            <p><?= e(format_date(new DateTimeImmutable('now'))) ?></p>
            <p class="muted">Each deploy pipeline run copies the current checkout here.</p>
        </article>
    </section>
</main>
<?php require __DIR__ . '/includes/footer.php'; ?>
