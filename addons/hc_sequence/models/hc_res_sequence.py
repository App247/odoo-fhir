# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Sequence(models.Model):    
    _name = "hc.res.sequence"    
    _description = "Sequence"        

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the sequence event. Subject Name + Type + Date.")
    date = fields.Datetime(
        string="Date", 
        help="When this sequence event was completed.")
    identifier_ids = fields.One2many(
        comodel_name="hc.sequence.identifier", 
        inverse_name="sequence_id", 
        string="Identifiers", 
        help="Unique ID for this particular sequence.")                
    type = fields.Selection(
        string="Type", 
        required="True", 
        selection=[
            ("aa", "AA"), 
            ("dna", "DNA"), 
            ("rna", "RNA")], 
        help="Type of a sequence.")                
    coordinate_system = fields.Integer(
        string="Coordinate System", 
        required="True", 
        help="Numbering used for sequence (0-based or 1-based).")                
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Who and/or what this is about.")                
    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen", 
        string="Specimen", 
        help="Specimen used for sequencing.")                
    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="The method for sequencing.")                
    performer_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Performer", 
        help="Who should be responsible for test result.")
    quantity = fields.Float(
        string="Quantity", 
        help="Quantity of the sequence.")                
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")                
    observed_seq = fields.Char(
        string="Observed Sequence", 
        help="Observed sequence.")                
    read_coverage = fields.Integer(
        string="Read Coverage", 
        help="Average number of reads representing a given nucleotide in the reconstructed sequence.")                
    pointer_ids = fields.One2many(
        comodel_name="hc.sequence.pointer", 
        inverse_name="sequence_id", 
        string="Pointers", 
        help="Pointer to next atomic sequence.")                
    reference_seq_id = fields.Many2one(
        comodel_name="hc.reference.sequence", 
        string="Reference Sequence", 
        help="Reference Sequence associated with this Sequence Resource.")      
    variant_ids = fields.One2many(
        comodel_name="hc.sequence.variant", 
        inverse_name="sequence_id", 
        string="Variants", 
        help="Variant info in this sequence.")                
    quality_ids = fields.One2many(
        comodel_name="hc.sequence.quality", 
        inverse_name="sequence_id", 
        string="Quality", 
        help="Sequence Quality.")                
    repository_ids = fields.One2many(
        comodel_name="hc.sequence.repository", 
        inverse_name="sequence_id", 
        string="Repositories", 
        help="External repository.")                              

class ReferenceSequence(models.Model):  
    _name = "hc.reference.sequence" 
    _description = "Reference Sequence"
           
    chromosome_id = fields.Many2one(
        comodel_name="hc.vs.chromosome.human", 
        string="Chromosome", 
        help="The chromosome containing the genetic finding.")                
    genome_build = fields.Char(
        string="Genome Build", 
        help='The Genome Build used for reference, following GRCh build versions e.g. "GRCh 37".')                
    reference_seq_id = fields.Many2one(
        comodel_name="hc.vs.sequence.reference.seq", 
        string="Reference Sequence ID", 
        required="True", 
        help="Reference identifier.")                
    reference_seq_pointer_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Reference Sequence Pointer", 
        help="A Pointer to another Sequence entity as refence sequence.")                
    reference_seq_string = fields.Char(
        string="Reference Seq String", 
        help="A Reference Sequence string.")                
    strand = fields.Integer(
        string="Strand", 
        required="True", 
        help='Strand of DNA. Available values are "1" for the plus strand and "-1" for the minus strand.')                
    window_start = fields.Integer(
        string="Window Start", 
        required="True", 
        help="Start position (inclusive) of the window on the reference sequence.")                
    window_end = fields.Integer(
        string="Window End", 
        required="True", 
        help="End position (exclusive) of the window on the reference sequence.")                

class SequenceVariant(models.Model):    
    _name = "hc.sequence.variant"   
    _description = "Sequence Variant"        

    sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Sequence", 
        help="Sequence associated with this variant.")                
    start = fields.Integer(
        string="Start", 
        help="Start position (inclusive) of the variant on the reference sequence.")                
    end = fields.Integer(
        string="End", 
        help="End position (exclusive) of the variant on the reference sequence.")                
    observed_allele = fields.Char(
        string="Observed Allele", 
        help="Nucleotide(s)/amino acids from start position to stop position of observed variant.")                
    reference_allele = fields.Char(
        string="Reference Allele", 
        help="Nucleotide(s)/amino acids from start position to stop position of reference variant.")                
    cigar = fields.Char(
        string="Cigar", 
        help="Extended CIGAR string for aligning the sequence with reference bases.")                
    # variant_pointer_id = fields.Many2one(
    #     comodel_name="hc.res.observation", 
    #     string="Variant Pointer", 
    #     help="A pointer to an Observation containing variant information.")                

class SequenceQuality(models.Model):    
    _name = "hc.sequence.quality"    
    _description = "Sequence Quality"        

    sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Sequence", 
        help="Sequence associated with this quality.")                
    type = fields.Selection(
        string="Quality Type", 
        required="True", 
        selection=[
            ("indel", "Indel"), 
            ("snp", "SNP"), 
            ("unknown", "Unknown")], 
        help="Indicates whether the account is presently used/useable or not.")
    standard_sequence_id = fields.Many2one(
        comodel_name="hc.vs.sequence.quality.standard.sequence", 
        string="Standard Sequence", 
        help="Standard sequence for comparison.")                
    start = fields.Integer(
        string="Start", 
        help="Start position (inclusive) of the sequence.")                
    end = fields.Integer(
        string="End", 
        help="End position (exclusive) of the sequence.")                
    score = fields.Float(
        string="Score", 
        help="Quality score.")                
    method_id = fields.Many2one(
        comodel_name="hc.vs.sequence.quality.method", 
        string="Method", help="Method for quality.")                
    truth_tp = fields.Float(
        string="Truth TP", 
        help="True positives from the perspective of the truth data.")                
    query_tp = fields.Float(
        string="Query TP", 
        help="True positives from the perspective of the query data.")                
    truth_fn = fields.Float(
        string="Truth FN", 
        help="False negatives.")
    query_fp = fields.Float(
        string="Query FP", 
        help="False positives.")
    gt_fp = fields.Float(
        string="Gt FP", 
        help="False positives where the non-REF alleles in the Truth and Query Call Sets match.")                
    precision = fields.Float(
        string="Precision", 
        help="Precision (PPV); QUERY.TP / (QUERY.TP + QUERY.FP).")
    recall = fields.Float(
        string="Recall", 
        help="Recall (sensitivity); TRUTH.TP / (TRUTH.TP + TRUTH.FN).")             
    f_score = fields.Float(
        string="f Score", 
        help="F-score.")                

class SequenceRepository(models.Model):    
    _name = "hc.sequence.repository"    
    _description = "Sequence Repository"        

    sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Sequence", 
        help="Sequence associated with this repository.")                
    type = fields.Selection(
        string="Repository Type", 
        required="True", 
        selection=[
            ("directlink", "Directlink"), 
            ("openapi", "Openapi"), 
            ("login", "Login"), 
            ("oauth", "Oauth"), 
            ("other", "Other")], 
        help="Indicates whether the account is presently used/useable or not.")
    url = fields.Char(
        string="URI", 
        help="URI of the repository.")                
    name = fields.Char(
        string="Name", 
        help="Name of the repository.")                
    dataset_id = fields.Char(
        string="Dataset Id", 
        help="Id of the dataset that used to call for dataset in repository.")
    variantset_id = fields.Char(
        string="Variantset Id", 
        help="Id of the variantset that used to call for variantset in repository.")
    readset_id = fields.Char(
        string="Readset Id", 
        help="Id of the read.")

class SequenceIdentifier(models.Model):    
    _name = "hc.sequence.identifier"    
    _description = "Sequence Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Sequence", 
        help="Sequence associated with this Sequence Identifier.")                

class SequencePointer(models.Model):    
    _name = "hc.sequence.pointer"    
    _description = "Sequence Pointer"        
    _inherit = ["hc.basic.association"]

    sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Sequence", 
        help="Sequence associated with this Sequence Pointer.")                
    pointer_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Pointer", 
        help="Pointer associated with this Sequence Pointer.")                

class ChormosomeHuman(models.Model):    
    _name = "hc.vs.chromosome.human"    
    _description = "Chromosome Human"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this chromosome human.")
    code = fields.Char(
        string="Code", 
        help="Code of this chromosome human.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.chromosome.human", 
        string="Parent", 
        help="Parent chromosome human.")

class SequenceReferenceSeq(models.Model):    
    _name = "hc.vs.sequence.reference.seq"    
    _description = "Sequence Reference Seq"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this sequence reference sequence.")
    code = fields.Char(
        string="Code", 
        help="Code of this sequence reference sequence.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.sequence.reference.seq", 
        string="Parent", 
        help="Parent sequence reference sequence.")

class SequenceQualityStandardSequence(models.Model):    
    _name = "hc.vs.sequence.quality.standard.sequence"    
    _description = "Sequence Quality Standard Sequence"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this sequence quality standard sequence.")
    code = fields.Char(
        string="Code", 
        help="Code of this sequence quality standard sequence.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.sequence.quality.standard.sequence", 
        string="Parent", 
        help="Parent sequence quality standard sequence.")

class SequenceQualityMethod(models.Model):    
    _name = "hc.vs.sequence.quality.method"    
    _description = "Sequence Quality Method"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this sequence quality method.")
    code = fields.Char(
        string="Code", 
        help="Code of this sequence quality method.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.sequence.quality.method", 
        string="Parent", 
        help="Parent sequence quality method.")
