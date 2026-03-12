<?php
/**
 * Papilotka theme functions
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// ── Theme setup ──────────────────────────────────────────────────────────────

add_action( 'after_setup_theme', function (): void {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'align-wide' );
	add_theme_support( 'html5', [
		'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script',
	] );

	load_theme_textdomain( 'papilotka', get_template_directory() . '/languages' );
} );

// ── Assets ───────────────────────────────────────────────────────────────────

add_action( 'wp_enqueue_scripts', function (): void {
	// Google Fonts
	wp_enqueue_style(
		'papilotka-fonts',
		'https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Work+Sans:wght@400;500;600&display=swap',
		[],
		null
	);

	// Theme JS
	wp_enqueue_script(
		'papilotka-theme',
		get_template_directory_uri() . '/assets/js/theme.js',
		[],
		wp_get_theme()->get( 'Version' ),
		[ 'strategy' => 'defer', 'in_footer' => true ]
	);
} );

// Same fonts in the editor
add_action( 'enqueue_block_editor_assets', function (): void {
	wp_enqueue_style(
		'papilotka-fonts-editor',
		'https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Work+Sans:wght@400;500;600&display=swap',
		[],
		null
	);
} );

// ── Block styles ─────────────────────────────────────────────────────────────

add_action( 'init', function (): void {
	// Button: ghost variant
	register_block_style( 'core/button', [
		'name'  => 'ghost',
		'label' => __( 'Ghost', 'papilotka' ),
	] );

	// Group: cinematic section (dark bg + generous padding)
	register_block_style( 'core/group', [
		'name'  => 'cinematic',
		'label' => __( 'Cinematic Section', 'papilotka' ),
	] );
} );

// ── Editor custom CSS ─────────────────────────────────────────────────────────

add_theme_support( 'editor-color-palette', [] ); // Disables default palette

add_action( 'after_setup_theme', function (): void {
	add_editor_style( 'assets/css/editor.css' );
} );
