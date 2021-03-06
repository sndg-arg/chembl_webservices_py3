__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class Metabolism(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ORGANISM_CHOICES = (
        ('Callithrix jacchus', 'Callithrix jacchus'),
        ('Canis lupus familiaris', 'Canis lupus familiaris'),
        ('Homo sapiens', 'Homo sapiens'),
        ('Mus musculus', 'Mus musculus'),
        ('Oryctolagus cuniculus', 'Oryctolagus cuniculus'),
        ('Rattus norvegicus', 'Rattus norvegicus'),
        )

    met_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key')
    drug_record = models.ForeignKey(CompoundRecords, on_delete=models.PROTECT,  blank=True, null=True, related_name='drug', help_text='Foreign key to compound_records. Record representing the drug or other compound for which metabolism is being studied (may not be the same as the substrate being measured)')
    substrate_record = models.ForeignKey(CompoundRecords, on_delete=models.PROTECT,  blank=True, null=True, related_name='substrate', help_text='Foreign key to compound_records. Record representing the compound that is the subject of metabolism')
    metabolite_record = models.ForeignKey(CompoundRecords, on_delete=models.PROTECT,  blank=True, null=True, related_name='metabolite', help_text='Foreign key to compound_records. Record representing the compound that is the result of metabolism')
    pathway_id = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text='Identifier for the metabolic scheme/pathway (may be multiple pathways from one source document)')
    pathway_key = models.CharField(max_length=50, blank=True, null=True, help_text='Link to original source indicating where the pathway information was found (e.g., Figure 1, page 23)')
    enzyme_name = models.CharField(max_length=200, blank=True, null=True, help_text='Name of the enzyme responsible for the metabolic conversion')
    target = models.ForeignKey(TargetDictionary, on_delete=models.PROTECT,  blank=True, null=True, db_column='enzyme_tid', help_text='Foreign key to target_dictionary. TID for the enzyme responsible for the metabolic conversion')
    met_conversion = models.CharField(max_length=200, blank=True, null=True, help_text='Description of the metabolic conversion')
    organism = models.CharField(max_length=100, blank=True, null=True, choices=ORGANISM_CHOICES, help_text='Organism in which this metabolic reaction occurs')
    tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text='NCBI Tax ID for the organism in which this metabolic reaction occurs')
    met_comment = models.CharField(max_length=1000, blank=True, null=True, help_text='Additional information regarding the metabolism (e.g., organ system, conditions under which observed, activity of metabolites)')
    enzyme_comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("drug_record", "substrate_record", "metabolite_record", "pathway_id", "enzyme_name",
                            "target", "tax_id"),)

# ----------------------------------------------------------------------------------------------------------------------


class MetabolismRefs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    REF_TYPE_CHOICES = (
        ('DAILYMED', 'DAILYMED'),
        ('DOI', 'DOI'),
        ('DailyMed', 'DailyMed'),
        ('FDA', 'FDA'),
        ('ISBN', 'ISBN'),
        ('OTHER', 'OTHER'),
        ('PMID', 'PMID'),
        )

    metref_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key')
    metabolism = models.ForeignKey(Metabolism, on_delete=models.PROTECT,  db_column='met_id', help_text='Foreign key to record_metabolism table - indicating the metabolism information to which the references refer')
    ref_type = models.CharField(max_length=50, choices=REF_TYPE_CHOICES, help_text="Type/source of reference (e.g., 'PubMed','DailyMed')")
    ref_id = models.CharField(max_length=200, blank=True, null=True, help_text='Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)')
    ref_url = models.CharField(max_length=400, blank=True, null=True, help_text='Full URL linking to the reference')
    downgraded = ChemblIntegerField(length=1, blank=True, null=True)
    downgrade_reason = models.CharField(max_length=4000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("metabolism", "ref_type", "ref_id"),)

# ----------------------------------------------------------------------------------------------------------------------


