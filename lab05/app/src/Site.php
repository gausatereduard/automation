<?php

declare(strict_types=1);

/**
 * Small helper library used by the static site and by the PHPUnit tests.
 *
 * The site is intentionally dependency-free at runtime. Composer is used
 * only to install PHPUnit for the build pipeline.
 */

function site_title(): string
{
    return 'Aurora Studio';
}

function site_tagline(): string
{
    return 'A small static website built with plain PHP.';
}

/**
 * @return array<string, string> map of file name => navigation label
 */
function nav_items(): array
{
    return [
        'index.php' => 'Home',
        'about.php' => 'About',
        'contact.php' => 'Contact',
    ];
}

function page_title(string $page): string
{
    $titles = [
        'index.php' => 'Home',
        'about.php' => 'About this site',
        'contact.php' => 'Contact',
    ];

    return $titles[$page] ?? 'Page not found';
}

function is_active(string $page, string $currentPage): bool
{
    return $page === $currentPage;
}

function current_year(): int
{
    return (int) date('Y');
}

function format_date(DateTimeInterface $date): string
{
    return $date->format('F j, Y');
}

/**
 * Escapes a value for safe output in HTML.
 */
function e(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/**
 * Renders the navigation list and marks the current page.
 */
function render_nav(string $currentPage): string
{
    $html = '<nav class="site-nav" aria-label="Main navigation"><ul>';

    foreach (nav_items() as $file => $label) {
        $active = is_active($file, $currentPage);

        $html .= '<li>';
        $html .= '<a href="' . e($file) . '"';
        $html .= $active ? ' class="is-active" aria-current="page"' : '';
        $html .= '>' . e($label) . '</a>';
        $html .= '</li>';
    }

    $html .= '</ul></nav>';

    return $html;
}

/**
 * Returns the copyright line displayed in the footer.
 */
function footer_text(int $year): string
{
    return '© ' . $year . ' ' . site_title();
}
