

CREATE TABLE `hao6v_list` (
  `id` mediumint unsigned NOT NULL AUTO_INCREMENT COMMENT '行号',
  `title` varchar(100) DEFAULT '' COMMENT '列表 标题',
  `image_url` varchar(100) DEFAULT '' COMMENT '图片 URI',
  `url_md5` varchar(32) not null comment 'md5 唯一标示',
  `click_num` smallint unsigned NOT NULL DEFAULT 0 COMMENT '点击量',
  `category_id` tinyint unsigned NOT NULL COMMENT '类型 关联 id ',
  `update_at` int unsigned not null COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电影 列表';

create table `hao6v_search` (
  `id` mediumint unsigned NOT NULL AUTO_INCREMENT COMMENT '行号',
  `title` varchar(200) DEFAULT '' COMMENT '列表 标题',
  `category` varchar(50) DEFAULT '' comment '类别',
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电影 列表';

CREATE TABLE `hao6v_content` (
  `id` mediumint unsigned NOT NULL AUTO_INCREMENT COMMENT '行号 与 list_id相同',
  `content` text COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电影 内容';


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
