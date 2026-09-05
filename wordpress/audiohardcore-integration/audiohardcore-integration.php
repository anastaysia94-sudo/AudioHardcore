<?php
/**
 * Plugin Name: AudioHardcore Integration
 * Description: Connects a WordPress site to an AudioHardcore installation and provides a compact library shortcode.
 * Version: 0.1.0
 * Author: AudioHardcore
 * License: GPL-2.0-or-later
 */
if (!defined('ABSPATH')) { exit; }
const AH_WP_OPTION = 'audiohardcore_api_base_url';
add_action('admin_menu', function () { add_options_page('AudioHardcore','AudioHardcore','manage_options','audiohardcore','ah_wp_settings_page'); });
add_action('admin_init', function () { register_setting('audiohardcore', AH_WP_OPTION, ['type'=>'string','sanitize_callback'=>function($value){return esc_url_raw(trim((string)$value));},'default'=>'']); });
function ah_wp_settings_page() {
    if (!current_user_can('manage_options')) { return; }
    $value = get_option(AH_WP_OPTION, '');
    ?>
    <div class="wrap"><h1>AudioHardcore Integration</h1><form method="post" action="options.php">
        <?php settings_fields('audiohardcore'); ?>
        <table class="form-table" role="presentation"><tr>
            <th scope="row"><label for="audiohardcore_api_base_url">AudioHardcore API URL</label></th>
            <td><input name="<?php echo esc_attr(AH_WP_OPTION); ?>" id="audiohardcore_api_base_url" type="url" class="regular-text" value="<?php echo esc_attr($value); ?>" placeholder="https://music.example.com" />
            <p class="description">Use the HTTPS base URL of your AudioHardcore installation.</p></td>
        </tr></table><?php submit_button(); ?>
    </form></div>
    <?php
}
add_shortcode('audiohardcore_library', function () {
    $base = rtrim((string)get_option(AH_WP_OPTION, ''), '/');
    if ($base === '') return '<p>AudioHardcore is not configured. Set the API URL under Settings &gt; AudioHardcore.</p>';
    $response = wp_remote_get($base . '/library/stats', ['timeout'=>8,'headers'=>['Accept'=>'application/json']]);
    if (is_wp_error($response)) return '<p>AudioHardcore is currently unavailable.</p>';
    $status = wp_remote_retrieve_response_code($response);
    $body = json_decode(wp_remote_retrieve_body($response), true);
    if ($status < 200 || $status >= 300 || !is_array($body)) return '<p>AudioHardcore returned an invalid response.</p>';
    $tracks = isset($body['tracks']) ? (int)$body['tracks'] : 0;
    $artists = isset($body['artists']) ? (int)$body['artists'] : 0;
    $albums = isset($body['albums']) ? (int)$body['albums'] : 0;
    return sprintf('<div class="audiohardcore-widget"><strong>AudioHardcore</strong><p>%d tracks · %d artists · %d albums</p><a href="%s">Open AudioHardcore</a></div>', $tracks, $artists, $albums, esc_url($base));
});
