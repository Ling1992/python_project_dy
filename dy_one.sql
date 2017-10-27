CREATE TABLE `dy_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',

  `title` varchar(100) DEFAULT '' COMMENT '列表 标题',
  `name` varchar(50) DEFAULT '' COMMENT '电影名称',
  `image_url` varchar(100) DEFAULT '' COMMENT '图片 URI',

  `click_amount` int(11) NOT NULL DEFAULT '0' COMMENT '点击量',

  `category_id` int(11) NOT NULL COMMENT '类型 关联 id ',
  `content_id` int(11) NOT NULL COMMENT '电影详情 id',
  `content_table_tag` int(11) NOT NULL COMMENT '分库 编号',

  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 列表';

CREATE TABLE `dy_category` (
  `id` int(4) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `name` varchar(50) DEFAULT '' COMMENT '类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 类型(大方向)';

INSERT INTO `dy_category` (`id`,`name`) VALUES (1, '最新');
INSERT INTO `dy_category` (`id`,`name`) VALUES (2, '国语');
INSERT INTO `dy_category` (`id`,`name`) VALUES (3, '微电影');
INSERT INTO `dy_category` (`id`,`name`) VALUES (4, '经典高清');
INSERT INTO `dy_category` (`id`,`name`) VALUES (5, '动画电影');
INSERT INTO `dy_category` (`id`,`name`) VALUES (6, '3D电影');
INSERT INTO `dy_category` (`id`,`name`) VALUES (7, '国剧');
INSERT INTO `dy_category` (`id`,`name`) VALUES (8, '日韩剧');
INSERT INTO `dy_category` (`id`,`name`) VALUES (9, '欧美剧');
INSERT INTO `dy_category` (`id`,`name`) VALUES (10, '综艺');

CREATE TABLE `dy_content_01` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `content` text COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 1';

CREATE TABLE `dy_content_02` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `content` text COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 2';

CREATE TABLE `dy_content_03` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `content` text COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 3';

CREATE TABLE `dy_content_04` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `content` text COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影 4';

CREATE TABLE `ip_collection` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `ip` varchar(15) NOT NULL COMMENT 'ip 地址',
  `request_url` varchar(255)  NOT NULL DEFAULT '' COMMENT '请求 uri',
  `user_agent` varchar(255)  NOT NULL DEFAULT '' COMMENT 'UA',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
  PRIMARY KEY (`id`),
  KEY `ip` (`ip`),
  KEY `create_date` (`create_date`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='记录 访问 ip';

CREATE TABLE `ip_pool` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '行号',
  `ip` varchar(15) NOT NULL COMMENT 'ip 地址',
  `port` int(5) NOT NULL COMMENT '端口',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '类型 1 http 2 https',
  `state` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否有效  0：有效 1：无效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idy` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='ip 池';

