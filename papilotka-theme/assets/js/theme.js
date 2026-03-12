/**
 * Papilotka theme — theme.js
 * Handles: sticky header shadow, scroll-reveal, smooth anchor scroll.
 */

( () => {
	'use strict';

	// ── Sticky header: add shadow + bg-opacity on scroll ──────────────────────

	const header = document.querySelector( '.site-header' );

	if ( header ) {
		const onScroll = () => {
			if ( window.scrollY > 20 ) {
				header.classList.add( 'is-scrolled' );
			} else {
				header.classList.remove( 'is-scrolled' );
			}
		};

		window.addEventListener( 'scroll', onScroll, { passive: true } );
		onScroll(); // run once on load
	}

	// ── Scroll-reveal: fade-in elements when they enter the viewport ──────────

	const revealObserver = new IntersectionObserver(
		( entries ) => {
			entries.forEach( ( entry ) => {
				if ( entry.isIntersecting ) {
					entry.target.classList.add( 'is-visible' );
					revealObserver.unobserve( entry.target );
				}
			} );
		},
		{ threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
	);

	document
		.querySelectorAll( '.reveal' )
		.forEach( ( el ) => revealObserver.observe( el ) );

	// ── Smooth scroll for anchor links ─────────────────────────────────────────

	document.querySelectorAll( 'a[href^="#"]' ).forEach( ( anchor ) => {
		anchor.addEventListener( 'click', ( e ) => {
			const id = anchor.getAttribute( 'href' );
			if ( id === '#' ) return;
			const target = document.querySelector( id );
			if ( ! target ) return;

			e.preventDefault();

			const headerHeight = header ? header.offsetHeight : 0;
			const top = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;

			window.scrollTo( { top, behavior: 'smooth' } );
		} );
	} );

} )();
