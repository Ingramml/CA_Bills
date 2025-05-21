-- ----------------------------------------------------------------------------+
-- capublic_Postgres.sql - Create all the capublic tables in PostgreSQL database.
-- This script is rewritten for PostgreSQL compatibility.
-- ----------------------------------------------------------------------------+

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS capublic;

-- -------------------------------------
-- Tables
-- -------------------------------------

DROP TABLE IF EXISTS capublic.bill_analysis_tbl CASCADE;
CREATE TABLE capublic.bill_analysis_tbl (
  analysis_id NUMERIC(22, 0) PRIMARY KEY,
  bill_id VARCHAR(20) NOT NULL,
  house VARCHAR(1),
  analysis_type VARCHAR(100),
  committee_code VARCHAR(6),
  committee_name VARCHAR(200),
  amendment_author VARCHAR(100),
  analysis_date TIMESTAMP,
  amendment_date TIMESTAMP,
  page_num NUMERIC(22, 0),
  source_doc BYTEA,
  released_floor VARCHAR(1),
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(20),
  trans_update TIMESTAMP
);

DROP TABLE IF EXISTS capublic.bill_detail_vote_tbl CASCADE;
CREATE TABLE capublic.bill_detail_vote_tbl (
  bill_id VARCHAR(20) NOT NULL,
  location_code VARCHAR(6) NOT NULL,
  legislator_name VARCHAR(50) NOT NULL,
  vote_date_time TIMESTAMP NOT NULL,
  vote_date_seq INTEGER NOT NULL,
  vote_code VARCHAR(5),
  motion_id INTEGER NOT NULL,
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  member_order INTEGER,
  session_date TIMESTAMP,
  speaker VARCHAR(1)
);

DROP TABLE IF EXISTS capublic.bill_history_tbl CASCADE;
CREATE TABLE capublic.bill_history_tbl (
  bill_id VARCHAR(20),
  bill_history_id NUMERIC(20, 0),
  action_date TIMESTAMP,
  action VARCHAR(2000),
  trans_uid VARCHAR(20),
  trans_update_dt TIMESTAMP,
  action_sequence INTEGER,
  action_code VARCHAR(5),
  action_status VARCHAR(60),
  primary_location VARCHAR(60),
  secondary_location VARCHAR(60),
  ternary_location VARCHAR(60),
  end_status VARCHAR(60)
);

DROP TABLE IF EXISTS capublic.bill_motion_tbl CASCADE;
CREATE TABLE capublic.bill_motion_tbl (
  motion_id NUMERIC(20, 0) PRIMARY KEY,
  motion_text VARCHAR(250),
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP
);

DROP TABLE IF EXISTS capublic.bill_summary_vote_tbl CASCADE;
CREATE TABLE capublic.bill_summary_vote_tbl (
  bill_id VARCHAR(20) NOT NULL,
  location_code VARCHAR(6) NOT NULL,
  vote_date_time TIMESTAMP NOT NULL,
  vote_date_seq INTEGER NOT NULL,
  motion_id INTEGER NOT NULL,
  ayes INTEGER,
  noes INTEGER,
  abstain INTEGER,
  vote_result VARCHAR(6),
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  file_item_num VARCHAR(10),
  file_location VARCHAR(50),
  display_lines VARCHAR(2000),
  session_date TIMESTAMP
);

DROP TABLE IF EXISTS capublic.bill_tbl CASCADE;
CREATE TABLE capublic.bill_tbl (
  bill_id VARCHAR(19) PRIMARY KEY,
  session_year VARCHAR(8) NOT NULL,
  session_num VARCHAR(2) NOT NULL,
  measure_type VARCHAR(4) NOT NULL,
  measure_num INTEGER NOT NULL,
  measure_state VARCHAR(40) NOT NULL,
  chapter_year VARCHAR(4),
  chapter_type VARCHAR(10),
  chapter_session_num VARCHAR(2),
  chapter_num VARCHAR(10),
  latest_bill_version_id VARCHAR(30),
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  current_location VARCHAR(200),
  current_secondary_loc VARCHAR(60),
  current_house VARCHAR(60),
  current_status VARCHAR(60),
  days_31st_in_print TIMESTAMP
);

DROP TABLE IF EXISTS capublic.bill_version_authors_tbl CASCADE;
CREATE TABLE capublic.bill_version_authors_tbl (
  bill_version_id VARCHAR(30) NOT NULL,
  type VARCHAR(15) NOT NULL,
  house VARCHAR(100),
  name VARCHAR(100),
  contribution VARCHAR(100),
  committee_members VARCHAR(2000),
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  primary_author_flg VARCHAR(1) DEFAULT 'N'
);

DROP TABLE IF EXISTS capublic.bill_version_tbl CASCADE;
CREATE TABLE capublic.bill_version_tbl (
  bill_version_id VARCHAR(30) PRIMARY KEY,
  bill_id VARCHAR(19) NOT NULL,
  version_num INTEGER NOT NULL,
  bill_version_action_date TIMESTAMP NOT NULL,
  bill_version_action VARCHAR(100),
  request_num VARCHAR(10),
  subject VARCHAR(1000),
  vote_required VARCHAR(100),
  appropriation VARCHAR(3),
  fiscal_committee VARCHAR(3),
  local_program VARCHAR(3),
  substantive_changes VARCHAR(3),
  urgency VARCHAR(3),
  taxlevy VARCHAR(3),
  bill_xml TEXT,
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP
);

DROP TABLE IF EXISTS capublic.codes_tbl CASCADE;
CREATE TABLE capublic.codes_tbl (
  code VARCHAR(5),
  title VARCHAR(2000)
);

DROP TABLE IF EXISTS capublic.committee_hearing_tbl CASCADE;
CREATE TABLE capublic.committee_hearing_tbl (
  bill_id VARCHAR(20),
  committee_type VARCHAR(2),
  committee_nr INTEGER,
  hearing_date TIMESTAMP,
  location_code VARCHAR(6),
  trans_uid VARCHAR(30),
  trans_update_date TIMESTAMP
);

DROP TABLE IF EXISTS capublic.daily_file_tbl CASCADE;
CREATE TABLE capublic.daily_file_tbl (
  bill_id VARCHAR(20),
  location_code VARCHAR(6),
  consent_calendar_code INTEGER,
  file_location VARCHAR(6),
  publication_date TIMESTAMP,
  floor_manager VARCHAR(100),
  trans_uid VARCHAR(20),
  trans_update_date TIMESTAMP,
  session_num VARCHAR(2),
  status VARCHAR(200)
);

DROP TABLE IF EXISTS capublic.law_section_tbl CASCADE;
CREATE TABLE capublic.law_section_tbl (
  id VARCHAR(100),
  law_code VARCHAR(5),
  section_num VARCHAR(30),
  op_statues VARCHAR(10),
  op_chapter VARCHAR(10),
  op_section VARCHAR(20),
  effective_date TIMESTAMP,
  law_section_version_id VARCHAR(100),
  division VARCHAR(100),
  title VARCHAR(100),
  part VARCHAR(100),
  chapter VARCHAR(100),
  article VARCHAR(100),
  history VARCHAR(1000),
  content_xml TEXT,
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP
);

DROP TABLE IF EXISTS capublic.law_toc_sections_tbl CASCADE;
CREATE TABLE capublic.law_toc_sections_tbl (
  id VARCHAR(100),
  law_code VARCHAR(5),
  node_treepath VARCHAR(100),
  section_num VARCHAR(30),
  section_order NUMERIC(22, 0),
  title VARCHAR(400),
  op_statues VARCHAR(10),
  op_chapter VARCHAR(10),
  op_section VARCHAR(20),
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  law_section_version_id VARCHAR(100),
  seq_num NUMERIC(22, 0)
);

DROP TABLE IF EXISTS capublic.law_toc_tbl CASCADE;
CREATE TABLE capublic.law_toc_tbl (
  law_code VARCHAR(5),
  division VARCHAR(100),
  title VARCHAR(100),
  part VARCHAR(100),
  chapter VARCHAR(100),
  article VARCHAR(100),
  heading VARCHAR(2000),
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  node_sequence NUMERIC(22, 0),
  node_level NUMERIC(22, 0),
  node_position NUMERIC(22, 0),
  node_treepath VARCHAR(100),
  contains_law_sections VARCHAR(1),
  history_note VARCHAR(350),
  op_statues VARCHAR(10),
  op_chapter VARCHAR(10),
  op_section VARCHAR(20)
);

DROP TABLE IF EXISTS capublic.legislator_tbl CASCADE;
CREATE TABLE capublic.legislator_tbl (
  district VARCHAR(5) NOT NULL,
  session_year VARCHAR(8),
  legislator_name VARCHAR(30),
  house_type VARCHAR(1),
  author_name VARCHAR(200),
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  middle_initial VARCHAR(1),
  name_suffix VARCHAR(12),
  name_title VARCHAR(34),
  web_name_title VARCHAR(34),
  party VARCHAR(4),
  active_flg VARCHAR(1) NOT NULL DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  active_legislator VARCHAR(1) DEFAULT 'Y'
);

DROP TABLE IF EXISTS capublic.location_code_tbl CASCADE;
CREATE TABLE capublic.location_code_tbl (
  session_year VARCHAR(8),
  location_code VARCHAR(6) NOT NULL,
  location_type VARCHAR(1) NOT NULL,
  consent_calendar_code VARCHAR(2),
  description VARCHAR(60),
  long_description VARCHAR(200),
  active_flg VARCHAR(1) DEFAULT 'Y',
  trans_uid VARCHAR(30),
  trans_update TIMESTAMP,
  inactive_file_flg VARCHAR(1)
);

DROP TABLE IF EXISTS capublic.veto_message_tbl CASCADE;
CREATE TABLE capublic.veto_message_tbl (
  bill_id VARCHAR(20),
  veto_date TIMESTAMP,
  message TEXT,
  trans_uid VARCHAR(20),
  trans_update TIMESTAMP
);

DROP TABLE IF EXISTS capublic.committee_agenda_tbl CASCADE;
CREATE TABLE capublic.committee_agenda_tbl (
  committee_code VARCHAR(200),
  committee_desc VARCHAR(1000),
  agenda_date TIMESTAMP,
  agenda_time VARCHAR(200),
  line1 VARCHAR(500),
  line2 VARCHAR(500),
  line3 VARCHAR(500),
  building_type VARCHAR(200),
  room_num VARCHAR(100)
);

-- -------------------------------------
-- Indexes
-- -------------------------------------
-- Add indexes after table creation (no length specifiers in PostgreSQL)

CREATE INDEX IF NOT EXISTS bill_analysis_bill_id_idx ON capublic.bill_analysis_tbl (bill_id);
CREATE INDEX IF NOT EXISTS author_votecode_idx ON capublic.bill_detail_vote_tbl (legislator_name, vote_code);
CREATE INDEX IF NOT EXISTS bill_detail_vote_id_idx ON capublic.bill_detail_vote_tbl (bill_id);
CREATE INDEX IF NOT EXISTS check_dup_detail_vote_idx ON capublic.bill_detail_vote_tbl (bill_id, vote_date_time, location_code, motion_id, legislator_name, vote_date_seq);
CREATE INDEX IF NOT EXISTS bill_history_id_idx ON capublic.bill_history_tbl (bill_id);
CREATE INDEX IF NOT EXISTS bill_summary_vote_id_idx ON capublic.bill_summary_vote_tbl (bill_id);
CREATE INDEX IF NOT EXISTS bill_summary_vote_mo_idx ON capublic.bill_summary_vote_tbl (motion_id);
CREATE INDEX IF NOT EXISTS check_dup_summary_vote_idx ON capublic.bill_summary_vote_tbl (bill_id, motion_id, vote_date_time, vote_date_seq, location_code);
CREATE INDEX IF NOT EXISTS bill_tbl_chapter_year_idx ON capublic.bill_tbl (chapter_year);
CREATE INDEX IF NOT EXISTS bill_tbl_measure_num_idx ON capublic.bill_tbl (measure_num);
CREATE INDEX IF NOT EXISTS bill_tbl_measure_type_idx ON capublic.bill_tbl (measure_type);
CREATE INDEX IF NOT EXISTS bill_tbl_session_idx ON capublic.bill_tbl (session_year);
CREATE INDEX IF NOT EXISTS bill_tbl_ltst_bill_ver_idx ON capublic.bill_tbl (latest_bill_version_id);
CREATE INDEX IF NOT EXISTS bill_version_auth_tbl_id_idx ON capublic.bill_version_authors_tbl (bill_version_id);
CREATE INDEX IF NOT EXISTS bill_version_auth_tbl_name_idx ON capublic.bill_version_authors_tbl (name);
CREATE INDEX IF NOT EXISTS bill_version_tbl_bill_id_idx ON capublic.bill_version_tbl (bill_id);
CREATE INDEX IF NOT EXISTS bill_version_tbl_version_idx ON capublic.bill_version_tbl (version_num);
CREATE INDEX IF NOT EXISTS committee_hear_bill_id_idx ON capublic.committee_hearing_tbl (bill_id);
CREATE INDEX IF NOT EXISTS daily_file_pub_date_idx ON capublic.daily_file_tbl (publication_date);
CREATE INDEX IF NOT EXISTS daily_file_tbl_bill_id_idx ON capublic.daily_file_tbl (bill_id);
CREATE INDEX IF NOT EXISTS law_section_tbl_pk ON capublic.law_section_tbl (id);
CREATE INDEX IF NOT EXISTS law_section_code_idx ON capublic.law_section_tbl (law_code);
CREATE INDEX IF NOT EXISTS law_section_id_idx ON capublic.law_section_tbl (law_section_version_id);
CREATE INDEX IF NOT EXISTS law_section_sect_idx ON capublic.law_section_tbl (section_num);
CREATE INDEX IF NOT EXISTS law_toc_sections_node_idx ON capublic.law_toc_sections_tbl (law_code, node_treepath);
CREATE INDEX IF NOT EXISTS law_toc_article_idx ON capublic.law_toc_tbl (article);
CREATE INDEX IF NOT EXISTS law_toc_chapter_idx ON capublic.law_toc_tbl (chapter);
CREATE INDEX IF NOT EXISTS law_toc_code_idx ON capublic.law_toc_tbl (law_code);
CREATE INDEX IF NOT EXISTS law_toc_division_idx ON capublic.law_toc_tbl (division);
CREATE INDEX IF NOT EXISTS law_toc_part_idx ON capublic.law_toc_tbl (part);
CREATE INDEX IF NOT EXISTS law_toc_title_idx ON capublic.law_toc_tbl (title);
CREATE INDEX IF NOT EXISTS location_code_tbl_pk1 ON capublic.location_code_tbl (location_code);
CREATE INDEX IF NOT EXISTS localtion_code_session_idx1 ON capublic.location_code_tbl (session_year);

-- --------------------------  E N D   O F  C O D E  --------------------------+