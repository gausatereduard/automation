<?php

declare(strict_types=1);

namespace Tests;

use PHPUnit\Framework\TestCase;

final class SiteTest extends TestCase
{
    public function testSiteTitleIsNotEmpty(): void
    {
        $this->assertNotSame('', site_title());
    }

    public function testSiteTaglineMentionsPhp(): void
    {
        $this->assertStringContainsStringIgnoringCase('php', site_tagline());
    }

    public function testNavigationContainsThreePages(): void
    {
        $items = nav_items();

        $this->assertCount(3, $items);
        $this->assertArrayHasKey('index.php', $items);
        $this->assertArrayHasKey('about.php', $items);
        $this->assertArrayHasKey('contact.php', $items);
    }

    public function testPageTitleIsHumanReadable(): void
    {
        $this->assertSame('About this site', page_title('about.php'));
        $this->assertSame('Contact', page_title('contact.php'));
    }

    public function testUnknownPageFallsBackToNotFoundTitle(): void
    {
        $this->assertSame('Page not found', page_title('missing.php'));
    }

    public function testIsActiveComparesPageNames(): void
    {
        $this->assertTrue(is_active('index.php', 'index.php'));
        $this->assertFalse(is_active('index.php', 'about.php'));
    }

    public function testCurrentYearIsTheCurrentYear(): void
    {
        $this->assertSame((int) date('Y'), current_year());
    }

    public function testFormatDateUsesReadableFormat(): void
    {
        $date = new \DateTimeImmutable('2026-11-16');

        $this->assertSame('November 16, 2026', format_date($date));
    }

    public function testEscapingSpecialCharacters(): void
    {
        $this->assertSame('&lt;script&gt;alert(&#039;x&#039;)&lt;/script&gt;', e("<script>alert('x')</script>"));
        $this->assertSame('Tom &amp; Jerry', e('Tom & Jerry'));
    }

    public function testNavigationMarksTheCurrentPage(): void
    {
        $html = render_nav('about.php');

        $this->assertStringContainsString('href="about.php" class="is-active"', $html);
        $this->assertStringContainsString('aria-current="page"', $html);
        $this->assertStringContainsString('href="index.php"', $html);
        $this->assertSame(1, substr_count($html, 'aria-current="page"'));
    }

    public function testFooterContainsYearAndSiteTitle(): void
    {
        $text = footer_text(2026);

        $this->assertStringContainsString('2026', $text);
        $this->assertStringContainsString(site_title(), $text);
    }
}
