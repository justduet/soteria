<?php
/*
Plugin Name:  Register Authorship of Works
Plugin URI:   http://soteria-001.anyy.com
Description:  Enables users to register their AI works and track their creative process
Version:      0.2
Author:       Anyy
Author URI:   http://soteria-001.anyy.com
License:      GPL2
License URI:  https://www.gnu.org/licenses/gpl-2.0.html
Domain Path:  /languages
*/


// Add custom field to gallery images
function custom_gallery_hash_field( $form_fields, $post ) {
    $custom_hash = get_post_meta( $post->ID, 'custom_hash', true );
    $form_fields['custom_hash'] = array(
        'label' => 'Custom Hash',
        'input' => 'html',
		'html' => "<textarea readonly>$custom_hash</textarea>",
//       'html' => "<b>$custom_hash</b>",
        'helps' => ''
    );
    return $form_fields;
}
add_filter( 'attachment_fields_to_edit', 'custom_gallery_hash_field', 10, 2 );

// Save custom field data
function save_custom_gallery_hash( $post, $attachment ) {
    if ( isset( $attachment['custom_hash'] ) ) {
        // update_post_meta( $post['ID'], 'custom_hash', sanitize_text_field( $attachment['custom_hash'] ) );
    }
    return $post;
}
add_filter( 'attachment_fields_to_save', 'save_custom_gallery_hash', 10, 2 );