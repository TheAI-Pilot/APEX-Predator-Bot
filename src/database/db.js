const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dataDir = path.join(__dirname, '../../data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

const db = new Database(path.join(dataDir, 'bot.sqlite'));

// Enable WAL mode for high performance and concurrency
db.pragma('journal_mode = WAL');

// Initialize database tables
db.exec(`
    CREATE TABLE IF NOT EXISTS guild_settings (
        guild_id TEXT PRIMARY KEY,
        mod_log_channel TEXT,
        welcome_channel TEXT,
        welcome_message TEXT DEFAULT 'Welcome to {server}, {user}!',
        welcome_enabled INTEGER DEFAULT 0,
        leave_channel TEXT,
        leave_message TEXT DEFAULT '{user} has left the server.',
        leave_enabled INTEGER DEFAULT 0,
        autorole_id TEXT,
        ticket_category_id TEXT,
        ticket_transcript_channel TEXT,
        automod_anti_spam INTEGER DEFAULT 0,
        automod_anti_invites INTEGER DEFAULT 0,
        automod_anti_links INTEGER DEFAULT 0,
        automod_anti_mass_mention INTEGER DEFAULT 0,
        automod_bad_words TEXT DEFAULT '[]'
    );

    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        moderator_id TEXT NOT NULL,
        reason TEXT NOT NULL,
        timestamp INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id TEXT NOT NULL,
        channel_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        created_at INTEGER NOT NULL,
        closed_at INTEGER,
        closed_by TEXT
    );

    CREATE TABLE IF NOT EXISTS reaction_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id TEXT NOT NULL,
        channel_id TEXT NOT NULL,
        message_id TEXT NOT NULL,
        role_id TEXT NOT NULL,
        emoji TEXT,
        label TEXT
    );
`);

module.exports = {
    db,

    // Guild Settings Helpers
    getGuildSettings(guildId) {
        const stmt = db.prepare('SELECT * FROM guild_settings WHERE guild_id = ?');
        let settings = stmt.get(guildId);
        if (!settings) {
            const insert = db.prepare(`
                INSERT INTO guild_settings (guild_id) VALUES (?)
            `);
            insert.run(guildId);
            settings = stmt.get(guildId);
        }
        return settings;
    },

    updateGuildSetting(guildId, column, value) {
        // Ensure record exists
        this.getGuildSettings(guildId);
        const stmt = db.prepare(`UPDATE guild_settings SET ${column} = ? WHERE guild_id = ?`);
        return stmt.run(value, guildId);
    },

    // Warnings
    addWarning(guildId, userId, moderatorId, reason) {
        const stmt = db.prepare(`
            INSERT INTO warnings (guild_id, user_id, moderator_id, reason, timestamp)
            VALUES (?, ?, ?, ?, ?)
        `);
        return stmt.run(guildId, userId, moderatorId, reason, Date.now());
    },

    getWarnings(guildId, userId) {
        const stmt = db.prepare(`
            SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY timestamp DESC
        `);
        return stmt.all(guildId, userId);
    },

    deleteWarning(guildId, warningId) {
        const stmt = db.prepare(`
            DELETE FROM warnings WHERE guild_id = ? AND id = ?
        `);
        return stmt.run(guildId, warningId);
    },

    clearWarnings(guildId, userId) {
        const stmt = db.prepare(`
            DELETE FROM warnings WHERE guild_id = ? AND user_id = ?
        `);
        return stmt.run(guildId, userId);
    },

    // Tickets
    createTicket(guildId, channelId, userId) {
        const stmt = db.prepare(`
            INSERT INTO tickets (guild_id, channel_id, user_id, status, created_at)
            VALUES (?, ?, ?, 'open', ?)
        `);
        return stmt.run(guildId, channelId, userId, Date.now());
    },

    getTicketByChannel(channelId) {
        const stmt = db.prepare('SELECT * FROM tickets WHERE channel_id = ?');
        return stmt.get(channelId);
    },

    closeTicket(channelId, closedBy) {
        const stmt = db.prepare(`
            UPDATE tickets 
            SET status = 'closed', closed_at = ?, closed_by = ? 
            WHERE channel_id = ?
        `);
        return stmt.run(Date.now(), closedBy, channelId);
    },

    // Reaction Roles
    addReactionRole(guildId, channelId, messageId, roleId, emoji, label) {
        const stmt = db.prepare(`
            INSERT INTO reaction_roles (guild_id, channel_id, message_id, role_id, emoji, label)
            VALUES (?, ?, ?, ?, ?, ?)
        `);
        return stmt.run(guildId, channelId, messageId, roleId, emoji, label);
    },

    getReactionRole(messageId, roleId) {
        const stmt = db.prepare('SELECT * FROM reaction_roles WHERE message_id = ? AND role_id = ?');
        return stmt.get(messageId, roleId);
    }
};
