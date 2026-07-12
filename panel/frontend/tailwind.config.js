/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			fontFamily: {
				display: ['Orbitron', 'sans-serif'],
				ui: ['Rajdhani', 'Exo 2', 'sans-serif'],
				mono: ['Share Tech Mono', 'monospace']
			},
			colors: {
				'cockpit-bg': '#0A0A0F',
				'cockpit-panel': '#111118',
				'cockpit-panel-light': '#1A1A24',
				'cockpit-accent': '#00AFFF',
				'cockpit-accent-glow': 'rgba(0, 175, 255, 0.55)',
				'cockpit-pink': '#FF00A0',
				'cockpit-pink-glow': 'rgba(255, 0, 160, 0.55)',
				'cockpit-danger': '#FF0055',
				'cockpit-text': '#EAEAEA',
				'cockpit-muted': '#9A9A9A',
				'cockpit-terminal': '#000000',
				'cockpit-terminal-green': '#00FF7F'
			},
			boxShadow: {
				'glow-accent': '0 0 14px rgba(0, 175, 255, 0.55)',
				'glow-pink': '0 0 14px rgba(255, 0, 160, 0.55)',
				'glow-green': '0 0 12px rgba(0, 255, 127, 0.5)',
				'glow-accent-lg': '0 0 24px rgba(0, 175, 255, 0.35)',
				'glow-pink-lg': '0 0 24px rgba(255, 0, 160, 0.35)'
			},
			animation: {
				'fade-in-up': 'fade-in-up 0.4s ease-out forwards',
				'pulse-glow': 'pulse-glow 2.5s ease-in-out infinite',
				'typing': 'typing 1.5s steps(40, end)'
			}
		}
	},
	plugins: []
};
