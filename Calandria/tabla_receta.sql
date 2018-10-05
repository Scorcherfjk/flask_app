/* To prevent any potential data loss issues, you should review this script in detail before running it outside the context of the database designer.*/
BEGIN TRANSACTION
SET QUOTED_IDENTIFIER ON
SET ARITHABORT ON
SET NUMERIC_ROUNDABORT OFF
SET CONCAT_NULL_YIELDS_NULL ON
SET ANSI_NULLS ON
SET ANSI_PADDING ON
SET ANSI_WARNINGS ON
COMMIT
BEGIN TRANSACTION
GO
CREATE TABLE squeegee.dbo.receta
	(
	id int NOT NULL IDENTITY (1, 1),
	pliego_goma varchar(50) NULL,
	pliego_mesa_alta varchar(50) NULL,
	green_tire varchar(50) NULL,
	presion_rodillo float(53) NULL,
	velocidad_maxima float(53) NULL,
	compuesto_a varchar(50) NULL,
	calibre_caliente_a float(53) NULL,
	ancho_squeegee_a float(53) NULL,
	ancho_pliego_a float(53) NULL,
	dima_a float(53) NULL,
	dimb_a float(53) NULL,
	compuesto_b varchar(50) NULL,
	calibre_caliente_b float(53) NULL,
	ancho_squeegee_b float(53) NULL,
	ancho_pliego_b float(53) NULL,
	dima_b float(53) NULL,
	dimb_b float(53) NULL,
	diferencia_yellow float(53) NULL,
	diferencia_red float(53) NULL,
	diferencia_blue float(53) NULL,
	fecha_modificacion datetime NOT NULL
	)  ON [PRIMARY]
GO
ALTER TABLE squeegee.dbo.receta ADD CONSTRAINT
	DF_receta_fecha_modificacion DEFAULT (getdate()) FOR fecha_modificacion
GO
ALTER TABLE squeegee.dbo.receta ADD CONSTRAINT
	PK_receta PRIMARY KEY CLUSTERED 
	(
	id
	) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]

GO
ALTER TABLE squeegee.dbo.receta SET (LOCK_ESCALATION = TABLE)
GO
COMMIT
